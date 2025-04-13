<template>
    <div class="welcome-container">
        <h1 class="fade-in">Chào mừng bạn đến với ứng dụng chatbot Viet Instruments</h1>
        <p class="fade-in delay">Khám phá kiến thức về các loại nhạc cụ truyền thống Việt Nam ngay bây giờ.</p>
        <router-link to="/chat"><button class="welcome-btn fade-in delay-more">Bắt đầu ngay</button></router-link>
    </div>
</template>

<script>
export default {
    name: "WelcomeView",
    methods: {
        showAlert() {
            alert("Chúc bạn có trải nghiệm tuyệt vời với Vue.js!");
        },
    },
};
</script>

<style scoped>
.welcome-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    text-align: center;
    background: linear-gradient(135deg, #f6d365, #fda085);
    color: #fff;
    font-family: Arial, sans-serif;
}

h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

p {
    font-size: 1.2rem;
    margin-bottom: 20px;
}

.welcome-btn {
    padding: 10px 20px;
    font-size: 1rem;
    color: #fda085;
    background: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: transform 0.2s, background 0.3s;
}

.welcome-btn:hover {
    background: #eee;
    transform: scale(1.05);
}

/* Hiệu ứng fade-in */
.fade-in {
    opacity: 0;
    animation: fadeIn 1s ease-in forwards;
}

.delay {
    animation-delay: 0.5s;
}

.delay-more {
    animation-delay: 1s;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>