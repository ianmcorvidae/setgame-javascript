/*
 * Stew Houston
 *
 * MIT/GPL
 *
 */
(function($) {
    $(window).load(function() {
        window.loaded = 1;
    });
    
    $.windowLoaded = function(fn) {
        var windowLoadedFn = window.loaded ? 
          (function(fn) { fn.call(window); }) : // the window has already loaded
          (function(fn) { $(window).load(fn); }); // the window hasn't loaded
        
        windowLoadedFn(fn);
    };
})(jQuery);
