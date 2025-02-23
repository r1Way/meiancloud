document.addEventListener('DOMContentLoaded', function () {
    // 获取所有的目标元素
    const scrollSection = document.querySelectorAll('.scroll-section');
    //创建 Intersection Observer 实例
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    // 当元素进入视口时，添加 visible 类
                    entry.target.classList.add('visible');
                } else {
                    // 当元素离开视口时，移除 visible 类
                    entry.target.classList.remove('visible');
                }
            });
        },
        {
            rootMargin: '0px', // 可以设置一个边距，提前触发
            threshold: 0.6 // 当图片的60%进入视口时触发
        }
    );

    // 开始观察目标元素
    scrollSection.forEach((section)=>{
        observer.observe(section);
    })
});