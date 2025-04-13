import createApiClient from "./api.service";

class PredictService {
    constructor(baseUrl = "/api/predict/") {
        this.api = createApiClient(baseUrl);
    }
    async predict(data) {
        const respone = await this.api.post("/", data);
        return respone;
    }
}
export default new PredictService();