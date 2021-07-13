function business_orders_search_caller(pattern_id) {
    let pattern = document.getElementById(pattern_id).value;
    let is_num = /^\d+$/.test(pattern);
    if (is_num)
        search_pattern(pattern_id, '', 'display_block', 'order_card_text_orderid', 'order_card');
    else
        search_pattern(pattern_id, '', 'display_block', 'order_card_text_sender_customername', 'order_card');
}