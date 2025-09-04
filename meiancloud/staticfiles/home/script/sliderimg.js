
//lxc 图片浮现
document.addEventListener('DOMContentLoaded', function() {
    // 获取图片元素
    var imgs = document.querySelectorAll('.fade-in-image');

    //console.log(img);

    imgs.forEach(img=>{
        // 创建一个IntersectionObserver实例
    var observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                // 当图片进入视口时，添加'visible'类
                img.classList.add('visible');
            } else {
                // 当图片离开视口时，移除'visible'类
                img.classList.remove('visible');
            }
        });
    }, {
        rootMargin: '0px', // 可以设置一个边距，提前触发
        threshold: 0.6 // 当图片的60%进入视口时触发
    });

    observer.observe(img);
    });

    

    // 开始观察图片元素

    // img.forEach(image=>{
    //     observer.observe(image);
    // })
    //observer.observe(img);
});