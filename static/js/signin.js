/**
 * index.js
 * - All our useful JS goes here, awesome!
 */
$(document).ready(function(){
    $(".username").focus(function(){
      $(".fa-user").css("color", "#e6173e");
      $(".fa-unlock-alt").css("color", "#000");
    });
    $(".password").focus(function(){
      $(".fa-unlock-alt").css("color", "#e6173e");
      $(".fa-user").css("color", "#000");
    });
    
  });
  
  $(document).ready(function(){
    $(".email").focus(function(){
      $(".fa-envelope").css("color", "#e6173e");
    });
    $(".name").focus(function(){
      $(".fa-user").css("color", "#e6173e");
    });
    $(".password").focus(function(){
      $(".fa-lock").css("color", "#e6173e");
    });
    $(".password-confirm").focus(function(){
      $(".fa-unlock-alt").css("color", "#e6173e");
    });
  });