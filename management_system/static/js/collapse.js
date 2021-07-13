var  flag = -1;

function category_section(elem,click_btn,collapse,collapse_open){
  var old_flag = flag;
  var category_collapse_open = document.getElementsByClassName(collapse_open);
  for(var i = 0;i<category_collapse_open.length;i++){
      category_collapse_open[i].className = collapse;
  }

    var category = document.getElementsByClassName(click_btn);
    var category_content = document.getElementsByClassName(collapse);
    
    for(var i = 0;i<=category.length;i++){
        if(elem == category[i]){
          flag = i
        }
    }
    if(old_flag == flag){
      category_content[flag].className = collapse;
      flag = -1;
    }else{
      category_content[flag].className = collapse_open;
    }
    
}