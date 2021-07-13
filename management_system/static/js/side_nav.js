
function control_side_navbar(bar_id,toggle_id){
    if(toggle_id == 'open'){
        side_navbar_toggle_open(bar_id)
    }
    if(toggle_id == 'close'){
        side_navbar_toggle_close(bar_id)
    }
  
}

function side_navbar_toggle_open(bar_id){
    document.getElementById(bar_id).style.left = '0px';
    document.getElementById(bar_id).style.transition = 'all 0.4s';
    document.getElementById('close').style.display = 'block';
    document.getElementById('open').style.display = 'none';

}

function side_navbar_toggle_close(bar_id){
    document.getElementById(bar_id).style.left = '-100%';
    document.getElementById(bar_id).style.transition = 'all 0.4s';
    document.getElementById('close').style.display = 'none';
    document.getElementById('open').style.display = 'block';

}