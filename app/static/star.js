$(document).ready(function() 
{
    var $star_rating = $('.star-rating');

    var SetRatingStar = function() 
    {  
      $star_rating.each(setStars);
    };
    
    function setStars() 
    {
      var ratingVal = parseInt($(this).find('input.rating-value').val());
      $(this).children().removeClass('fa-star').addClass('fa-star-o');
      for(var i = 0; i < ratingVal; i ++)
        $(this).children().eq(i).removeClass('fa-star-o').addClass('fa-star');  
    }
    
    $star_rating.on('click', '.fa', function() 
    {  
        if (!$(this).parent().hasClass('main'))
        {
            $(this).siblings('input.rating-value').val($(this).index() + 1);
            setStars.call($(this).parent());
            
            var rate = ($('input.rating-value').val());
            var url = $("#rating_system").attr("text") + "/" + rate;
            window.location.href = url;
        }
    });
    SetRatingStar();

    function refreshPage()
    {
      window.location.reload();
    }
  
    $(function()
    {
        $('[data-toggle="tooltip"]').tooltip()
    })
});