<template>
    <div class="main">
        <AppHeader />
        <div class="main-container">
            <div class="chat-container">
            <!-- Hiển thị tin nhắn -->
                <div class="messages" ref="messages">
                    <div v-for="(message, index) in chatMessages" :key="index" 
                    :class="['message', message.sender, {'typing': message.typing}]">
                        <span v-if="message.text">{{ message.text }}</span>
                        <img v-if="message.image" :src="message.image" alt="Image" class="message-image" />
                    </div>
                </div>

                <!-- Ô nhập và nút gửi -->
                <div class="input-main">
                    <div class="input-box">
                        <div class="preview" v-if="imagePreview">
                            <img :src="imagePreview" alt="Ảnh đã chọn" class="preview-image" />
                            <button class="remove-image-btn" @click="removeSelectedImage"><i class="fa-solid fa-xmark"></i></button>
                        </div>
                        <div class="ask-box">
                            <textarea v-model="userMessage" placeholder="Enter your question..." @keyup.enter="sendMessage"
                            class="input-textarea"></textarea>
                            <input type="file" id="fileInput" accept="image/*" @change="onImageSelected" />
                            <label for="fileInput" class="file-label"><i class="fa-solid fa-image"></i></label>
                            <button @click="sendMessage"><i class="fa-solid fa-arrow-up"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"; // Import thư viện axios để gửi request
import PredictService from "../services/predict.service";
import AppHeader from "@/components/AppHeader.vue";

export default {
    name: "ChatBox",
    components: {
        AppHeader
    },
    data() {
        return {
            userMessage: "", // User's input message
            chatMessages: [
                { text: "Chào bạn! Mình có thể giúp gì cho bạn?", sender: "bot" }
            ], // Message history
            selectedImage: null, // Currently selected image
            imagePreview: null, // Temporary URL for selected image
            persistedImage: null, // Persisted image for reuse
            isFirstImageMessage: true, // Flag to control image display in chat
        };
    },
    methods: {
        async sendMessage() {
            // Nếu ảnh được chọn lần đầu hoặc đã lưu ảnh, hiển thị ảnh một lần
            if (this.isFirstImageMessage) {
                if (this.selectedImage) {
                    this.chatMessages.push({ image: this.imagePreview, sender: "user" });

                    // Lưu ảnh đã chọn để sử dụng cho các câu hỏi sau
                    this.persistedImage = this.selectedImage;
                    this.persistedImagePreview = this.imagePreview;

                    // Reset ảnh tạm thời sau khi lưu
                    this.selectedImage = null;
                    this.imagePreview = null;

                    // Đánh dấu ảnh đã được gửi lần đầu
                    this.isFirstImageMessage = false;
                }
            }

            // Thêm câu hỏi của người dùng vào khung chat
            if (this.userMessage.trim() !== "") {
                this.chatMessages.push({ text: this.userMessage, sender: "user" });
            } else {
                this.chatMessages.push({ text: "Bạn muốn hỏi điều gì về bức ảnh này?", sender: "bot" });
                this.scrollToBottom(); // Cuộn xuống cuối cùng
                return;
            }

            // Nếu chưa có ảnh nào được gửi, thông báo yêu cầu tải ảnh
            if (!this.persistedImage) {
                this.chatMessages.push({ text: "Bạn vui lòng cung cấp ảnh cho câu hỏi này!", sender: "bot" });
                this.scrollToBottom(); // Cuộn xuống cuối cùng
                return;
            }

            // Tạo dữ liệu form để gửi lên API
            const formData = new FormData();
            formData.append("question", this.userMessage.trim());
            formData.append("image", this.persistedImage);

            // Reset nội dung tin nhắn sau khi gửi
            this.userMessage = "";

            try {
                // Hiển thị "đang nhập..." trước khi có kết quả
                this.typeEffect("...");
                
                // Gửi dữ liệu đến API
                const response = await PredictService.predict(formData);
                console.log("API Response:", response);

                // Xóa tin nhắn "đang nhập..." và thêm câu trả lời thực sự
                if (response.data && response.data.answer) {
                    // Xóa tin nhắn "đang suy nghĩ..."
                    this.chatMessages.pop();
                    // Sử dụng hiệu ứng đánh máy cho câu trả lời thực sự
                    this.typeEffect(response.data.answer);
                } else {
                    // Xóa tin nhắn "đang suy nghĩ..."
                    this.chatMessages.pop();
                    this.typeEffect("Sorry, no answer was received!");
                }
            } catch (error) {
                console.error("Error sending request:", error);
                // Xóa tin nhắn "đang suy nghĩ..."
                this.chatMessages.pop();
                this.typeEffect("Sorry, an error occurred!");
            } finally {
                this.scrollToBottom();
            }
        },

        typeEffect(fullText) {
            let typingText = "";
            let index = 0;
            
            // Thêm một tin nhắn mới từ bot với class typing
            this.chatMessages.push({ text: "", sender: "bot", typing: true });
            const messageIndex = this.chatMessages.length - 1;

            let typingInterval = setInterval(() => {
                if (index < fullText.length) {
                    typingText += fullText[index];
                    this.chatMessages[messageIndex].text = typingText;
                    index++;
                    this.scrollToBottom();
                } else {
                    // Hoàn thành đánh máy, loại bỏ trạng thái đánh máy
                    this.chatMessages[messageIndex].typing = false;
                    clearInterval(typingInterval);
                }
            }, 50); // Tốc độ đánh máy, có thể điều chỉnh tốc độ này
        },

        onImageSelected(event) {
            // Xử lý ảnh khi người dùng chọn
            this.selectedImage = event.target.files[0];
            this.imagePreview = URL.createObjectURL(this.selectedImage);

            // Đặt lại cờ để cho phép hiển thị ảnh lần đầu
            this.isFirstImageMessage = true;
        },
        removeSelectedImage() {
            // Xóa ảnh được chọn hoặc đã lưu
            this.selectedImage = null;
            this.imagePreview = null;
            this.persistedImage = null;
            this.persistedImagePreview = null;
            this.isFirstImageMessage = true; // Cho phép gửi ảnh lại nếu cần

            // Đặt lại input file
            const fileInput = document.getElementById("fileInput");
            if (fileInput) {
                fileInput.value = null;
            }
        },
        scrollToBottom() {
            // Cuộn xuống cuối khung chat
            this.$nextTick(() => {
                const messagesContainer = this.$refs.messages;
                if (messagesContainer) {
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }
            });
        },
    },
    mounted() {
        // Cuộn xuống cuối khung chat khi khởi động
        this.scrollToBottom();
    },

};


</script>


<style scoped>
/* Tổng thể khung chat */
.main{
    display: flex;
    height: 100vh;
    width: 100%;
    justify-content: space-between;
}

.main-container{
    width: 100%;
    display: flex;
    justify-content: center;
}

.chat-container {
    width: 80%;
    /* max-width: 600px; */
    /* margin: 60px auto; */
    border-radius: 10px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 100%;
    background-color: #585757;
    box-shadow: rgba(153, 153, 155, 0.2) 0px 7px 29px 0px;
}   


/* Khu vực hiển thị tin nhắn */
.messages {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    /* Khoảng cách giữa các tin nhắn */
}

/* Tin nhắn của bot (trái) */
.message.bot {
    align-self: flex-start;
    background-color: #000000;
    /* Nền xám đậm */
    color: #fff;
    /* Chữ trắng */
    padding: 10px 15px;
    border-radius: 15px 15px 15px 0;
    /* Bo góc cho tin nhắn bot */
    max-width: 70%;
    font-size: 14px;
    line-height: 1.5;
    word-wrap: break-word;
}

/* Tin nhắn của người dùng (phải) */
.message.user {
    align-self: flex-end;
    background-color: #d4d4d4;
    color: black;
    padding: 10px 15px;
    border-radius: 15px 15px 0 15px;
    max-width: 70%;
    font-size: 14px;
    line-height: 1.5;
    word-wrap: break-word;
}

/* Tin nhắn nhiều dòng sẽ tự động xuống hàng */
.message {
    display: inline-block;
    word-break: break-word;
}

/* Hình ảnh trong tin nhắn */
.message-image {
    /* max-width: 100%; */
    width: 224px;
    height: 224px;
    border-radius: 10px;
    margin-top: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.input-main{
    display: flex;
    width: 100%;
    justify-content: center;
    margin-bottom: 15px;
}

/* Khu vực nhập */
.input-box {
    display: flex;
    align-items: center;
    flex-direction: column;
    width: 70%;
    padding: 10px;
    border-radius: 15px;
    border-top: 1px solid #ddd;
    background-color: #f4f7f6;
    gap: 10px;
    /* Khoảng cách giữa các thành phần */
}

.ask-box{
    width: 100%;
    display: flex;
    align-items: center;
}

/* Ô nhập tin nhắn */
input[type="text"] {
    flex: 1;
    padding: 12px 15px;
    border: 1px solid #ddd;
    border-radius: 20px;
    font-size: 14px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
}

input[type="text"]:focus {
    outline: none;
    border-color: #4caf50;
    box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
}

/* Ô nhập tin nhắn (textarea) */
.input-textarea {
    flex: 1;
    padding: 12px 15px;
    border: 1px solid #ddd;
    border-radius: 20px;
    font-size: 14px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
    resize: none;
    overflow: hidden;
    line-height: 1.5;
    min-height: 40px;
    max-height: 100px;
    background-color: #fff;
    width: 60%;
    margin: 5px;
}

.input-textarea:focus {
    outline: none;
    border-color: #000;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

/* Nút thêm ảnh */
input[type="file"] {
    display: none;
}

.file-label {
    padding: 10px 15px;
    font-size: 14px;
    font-weight: bold;
    color: #fff;
    background-color: #000;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.file-label:hover {
    background-color: #302f2f;
}

/* Nút gửi */
button {
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
    color: #fff;
    background-color: #000;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    margin: 2.5px;
}

button:hover {
    background-color:  #302f2f;
}

button:active {
    transform: scale(0.98);
}

/* Hiển thị ảnh đã chọn */
.preview {
    display: flex;
    position: relative;
    /* gap: 5px; */
}

.preview-image {
    max-width: 80px;
    max-height: auto;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Nút xóa ảnh */
.remove-image-btn {
    background: #ffff;
    color: #000;
    font-size: 12px;
    border: none;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    /* height: 12pxs */
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    position: absolute;
    top: -10px;
    right: -10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    padding: 0;
}

.remove-image-btn:hover {
    background: #b9b7b7
}

/* Hiệu ứng con trỏ nhấp nháy cho tin nhắn đang đánh máy */
.message.bot.typing::after {
    content: "|";
    display: inline-block;
    animation: blink 0.8s infinite;
    margin-left: 2px;
}

@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}

</style>