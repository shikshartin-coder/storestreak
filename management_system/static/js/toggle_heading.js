function open_category(elem, class1, class2, icon1, icon2) {
    var category = document.getElementsByClassName(class1);
    var category_products = document.getElementsByClassName(class2);
    var icon1_class = document.getElementsByClassName(icon1)
    var icon2_class = document.getElementsByClassName(icon2)


    var flag;
    for (var i = 0; i < category.length; i++) {
        if (category[i] == elem) {
            flag = i;
        }
    }

    if (category_products[flag].className == class2 + ' open') {
        category_products[flag].className = class2 + ' close';
        icon1_class[flag].className = icon1 + ' close';
        icon2_class[flag].className = icon2 + ' open';
    } else {
        category_products[flag].className = class2 + ' open';
        icon1_class[flag].className = icon1 + ' open';
        icon2_class[flag].className = icon2 + ' close';
    }
}