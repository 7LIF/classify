"user strict";

(function () {
  //===== Prealoder

  window.onload = function () {
    window.setTimeout(fadeout, 500);
  };

  function fadeout() {
    document.querySelector(".preloader").style.opacity = "0";
    document.querySelector(".preloader").style.display = "none";
  }

  /*=====================================
    Sticky
    ======================================= */
  window.onscroll = function () {
    var header_navbar = document.querySelector(".navbar-area");
    var sticky = header_navbar.offsetTop;

    if (window.pageYOffset > sticky) {
      header_navbar.classList.add("sticky");
    } else {
      header_navbar.classList.remove("sticky");
    }

    // show or hide the back-top-top button
    var backToTo = document.querySelector(".scroll-top");
    if (
      document.body.scrollTop > 50 ||
      document.documentElement.scrollTop > 50
    ) {
      backToTo.style.display = "flex";
    } else {
      backToTo.style.display = "none";
    }
  };

  // WOW active
  new WOW().init();

  // for menu scroll
  var pageLink = document.querySelectorAll(".page-scroll");

  pageLink.forEach((elem) => {
    elem.addEventListener("click", (e) => {
      e.preventDefault();
      document.querySelector(elem.getAttribute("href")).scrollIntoView({
        behavior: "smooth",
        offsetTop: 1 - 60,
      });
    });
  });

  //===== mobile-menu-btn
  let navbarToggler = document.querySelector(".mobile-menu-btn");
  if (navbarToggler)
    navbarToggler.addEventListener("click", function () {
      navbarToggler.classList.toggle("active");
    });
})();
$(document).ready(function () {
  $(".img-alt").click(function () {
    $("#current").attr("src", $(this).attr("src"));
  });

  if ($("#img").attr("src")) {
    $("#main_image").hide();
    $("#main_image_label").hide();
  }
  if ($("#img2").attr("src")) {
    $("#image1").hide();
    $("#image1_label").hide();
  }

  if ($("#img3").attr("src")) {
    $("#image2").hide();
    $("#image2_label").hide();
  }

  if ($("#img4").attr("src")) {
    $("#image3").hide();
    $("#image3_label").hide();
  }

  if ($("#img5").attr("src")) {
    $("#image4").hide();
    $("#image4_label").hide();
  }

  $(".delete_image_click").click(function () {
    var clickedElement = $(this); // Store the clicked element
    var dataImg = $(this).attr("data-img");
    var type = $(this).attr("data-type");
    var urlParams = new URLSearchParams(window.location.search);
    var item = urlParams.get("item_id");
    $.ajax({
      url: "/account/removeImage",
      type: "POST",
      data: JSON.stringify({
        dataImg: dataImg,
        type: type + "_url",
        item: item,
      }), // Request data in JSON format
      contentType: "application/json",
      success: function (response) {
        // Handle the successful response
        console.log(response);
        if (response == "success") {
          clickedElement.hide(); // Hide the clicked element
          $("#" + type).show();
          $("#" + type + "_label").show();
          if (type == "main_image") {
            $("#" + type).prop("required", true);
          }
        }
      },
      error: function (xhr, status, error) {
        // Handle errors
        console.log(error);
      },
    });
  });

  $(".toggle_favorite").click(function () {
    var clickedElement = $(this); // Store the clicked element
    var item = $(this).attr("data-id");
    $.ajax({
      url: "/account/toggle_favorite",
      type: "POST",
      data: JSON.stringify({
        item_id: item,
      }), // Request data in JSON format
      contentType: "application/json",
      success: function (response) {
        if (response == "add") {
          clickedElement
            .find("i")
            .addClass("fa-heart favorited")
            .removeClass("fa-heart-o ");
        } else if (response == "remove") {
          clickedElement
            .find("i")
            .removeClass("fa-heart favorited")
            .addClass("fa-heart-o");
        }
      },
      error: function (xhr, status, error) {
        console.log(error);
      },
    });
  });
});
