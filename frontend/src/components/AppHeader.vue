<template>
    <nav class="navbar">
        <div class="navbar-brand-container">
            <a href="/" class="navbar-brand">
                <span class="brand-text"><i class="fa-brands fa-old-republic"></i></span>
                <span class="brand-text">Viet Instruments</span>
            </a>
            <div class="navbar-nav">
                <!-- <li class="nav-item"><b>Home</b></li>
                <li class="nav-item"><b>Contact</b></li>     -->
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: "app-header",
};
</script>

<style scoped>
.logo {
    width: 50px;
    height: auto;
}

.brand-text {
    font-size: 18px;
    font-weight: bold;
    color: #fff; /* Chữ trắng */
    white-space: nowrap;
}

.navbar {
    background-color: #232222; /* Nền đen */
    height: 100vh;
    width: 250px;
    box-shadow: 0 4px 4px 0 rgba(255, 255, 255, 0.1);
    display: flex;
}

.navbar-brand-container{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    height: 100%;
}

.navbar-brand{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

span{
    font-size: 40px;
}

.navbar-nav{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.navbar-nav .nav-item{
    color: #fff;
}
</style>
