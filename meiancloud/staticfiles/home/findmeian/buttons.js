// 获取所有按钮
const buttons = document.querySelectorAll('.buttons button');

// 为每个按钮添加点击事件监听器
buttons.forEach(button => {
    button.addEventListener('click', function() {
        // 获取目标区域的 ID
        const targetId = this.getAttribute('data-target');
        // 获取目标区域元素
        const targetSection = document.getElementById(targetId);
        //获取header高度
        const headerHeight = document.querySelector('header').offsetHeight;
        //计算偏移后的位置
        // 计算偏移后的滚动位置
        const offsetPosition = targetSection.offsetTop - headerHeight;
        // 平滑滚动到目标区域
        // targetSection.scrollIntoView({ behavior: 'smooth' });
        // 平滑滚动到偏移后的位置
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    });
});
