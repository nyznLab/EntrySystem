$(function() {
    $("td").on("mouseenter", function() {
      //js主要利用offsetWidth和scrollWidth判断是否溢出。
      //在这里scrollWidth是包含内容的完全高度，offsetWidth是当前表格单元格的宽度。
      if (this.offsetWidth < this.scrollWidth) {
        var that = this;
        var text = $(this).text();
        window.layer.tips(text, that, {
          tips: 1,
          time: 2000
        });
      }
    });
  })