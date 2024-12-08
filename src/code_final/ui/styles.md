<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.0/css/all.min.css">

<style>
    #input-container {
        position: fixed;
        bottom: 0;
        width: 100%;
        padding: 10px;
        background-color: white;
        z-index: 100;
    }
    h1, h2 {
        font-weight: bold;
        background: -webkit-linear-gradient(145deg, rgba(2,97,56,1) 0%, rgba(2,163,94,1) 100%);
        background: linear-gradient(145deg, rgba(2,97,56,1) 0%, rgba(2,163,94,1) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline;
        font-size: 8em;
    }
    .user-avatar {
        float: right;
        width: 50px;
        height: 50px;
        margin-left: 5px;
        margin-bottom: -10px;
        border-radius: 50%;
        object-fit: cover;
    }
    .bot-avatar {
        float: left;
        width: 50px;
        height: 50px;
        margin-right: 5px;
        border-radius: 50%;
        object-fit: cover;
    }
</style>
