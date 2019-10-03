jQuery(document).ready(function($){

  $(".gallery-photo .images-preview").each(function(){
    $(this).attr("data-fancybox", $(this).attr("data-fancybox-group"));
  });

  $('[data-fancybox]').fancybox({

    beforeShow : function(e, instance) {
        caption = instance.opts.$orig.parent().find(".caption").html()
        if ($(".fancybox-thumbs").length > 0) {
           // if we have thumbs
           if ($(".fancybox-thumbs .caption").length == 0) $(".fancybox-thumbs").append("<div class='caption'></div>");
           $(".fancybox-thumbs .caption").html(caption);
        }
        else {
           // if there is no thumbs, we need to add text somewhere else
           if ($(".fancybox-container .fullcaption").length == 0) $(".fancybox-container").append("<div class='fullcaption'></div>");
           $(".fancybox-container .fullcaption").html(caption);
        }
    },
  });

});
