document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".add-to-wishlist");
  
    buttons.forEach((btn) => {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        const productId = this.dataset.productId;
  
        fetch("/favorite/toggle/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ product_id: productId }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.status === "added") {
              this.querySelector("i").classList.remove("fa-heart-o");
              this.querySelector("i").classList.add("fa-heart");
            } else if (data.status === "removed") {
              this.querySelector("i").classList.remove("fa-heart");
              this.querySelector("i").classList.add("fa-heart-o");
            }
          });
      });
    });
  
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });