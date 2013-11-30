$(function() {
  $('div.item a.vote').bind('click', function() {
    var id = $(this).parents('div.item').attr('id').split('_')[1];
    var vote_type = $(this).hasClass('like') ? 'like' : 'dislike';
    if ($(this).hasClass('selected')) {
      $.post('/dislike/', {id : id, type : vote_type}, function(json) {
        $(this).removeClass('selected');
        $('p.score', '#item_' + id).html(json.score);
        alert('s');
      }
    } else {
      $.post('/like/', {id : id, type : vote_type}, function(json) {
        $(this).removeClass('selected');
        $('p.score', '#item_' + id).html(json.score);
        alert('u');
      }
    }
  });
});

