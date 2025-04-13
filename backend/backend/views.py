import torch
from transformers import ViTModel, ViTImageProcessor, AutoTokenizer, AutoModel
from PIL import Image
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Đường dẫn tới file CSV
csv_path = r'C:\Users\HP\OneDrive\Documents\Dang\CourseFile\Project\NLN\Report\web\backend\backend\data\instrument_train.csv'
data = pd.read_csv(csv_path)

# Xác định output_dim
unique_answers = data['answer'].unique()
output_dim = len(unique_answers)
print(f"Number of unique answers: {output_dim}")

# Label Encoder
label_encoder = LabelEncoder()
label_encoder.fit(data['answer'])

# Load các mô hình
feature_extractor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')
model_vit = ViTModel.from_pretrained('google/vit-base-patch16-224')
tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base')
model_bert = AutoModel.from_pretrained('vinai/phobert-base')

# Định nghĩa mô hình VQA
class QAModel(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(QAModel, self).__init__()
        self.fc1 = torch.nn.Linear(input_dim, hidden_dim)
        self.bn1 = torch.nn.BatchNorm1d(hidden_dim)
        self.dropout = torch.nn.Dropout(0.3)
        self.fc2 = torch.nn.Linear(hidden_dim, output_dim)
        self.relu = torch.nn.ReLU()
    
    def forward(self, combined_features):
        x = self.fc1(combined_features)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# Kiểm tra file model
model_path = r'C:\Users\HP\OneDrive\Documents\Dang\CourseFile\Project\NLN\Report\web\backend\backend\models\instrument_classifier.pth'



# Khởi tạo model và load weights
input_dim = 768 + 768  # 768 cho ViT và 768 cho BERT
hidden_dim = 512
model = QAModel(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim)
print("Model state_dict keys:", model.state_dict().keys())
model.load_state_dict(model.state_dict())
model.eval()

# API xử lý yêu cầu VQA
class VqaAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            # Nhận ảnh và câu hỏi
            image_file = request.FILES.get('image', None)
            question_text = request.data.get('question', None)

            if not image_file or not question_text:
                return JsonResponse({"error": "Missing image or question"}, status=status.HTTP_400_BAD_REQUEST)

            if not question_text.strip():
                return JsonResponse({"error": "Question cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

            # Xử lý ảnh
            try:
                image = Image.open(image_file).convert('RGB')
            except Exception as e:
                return JsonResponse({"error": f"Invalid image format: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            image_inputs = feature_extractor(images=image, return_tensors="pt")
            image_features = model_vit(**image_inputs).last_hidden_state[:, 0, :]

            # Tokenize câu hỏi
            question_inputs = tokenizer(question_text, return_tensors="pt", truncation=True, padding=True)
            question_features = model_bert(**question_inputs).last_hidden_state[:, 0, :]

            # Kết hợp đặc trưng ảnh và câu hỏi
            combined_features = torch.cat((image_features, question_features), dim=1).squeeze()

            # Dự đoán câu trả lời
            output = model(combined_features.unsqueeze(0))  # Add batch dimension
            _, predicted = torch.max(output, 1)
            predicted_index = predicted.item()

            # Kiểm tra predicted_index hợp lệ
            if predicted_index >= len(label_encoder.classes_):
                return JsonResponse({"error": "Prediction index out of range"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Decode câu trả lời
            answer = label_encoder.inverse_transform([predicted_index])[0]

            return JsonResponse({"question": question_text, "answer": answer}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
