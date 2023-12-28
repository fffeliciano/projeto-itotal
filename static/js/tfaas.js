$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-tfaa .modal-content").html("");
          $("#modal-tfaa").modal("show");
        },
        success: function (data) {
          $("#modal-tfaa .modal-content").html(data.html_form);
        }
      });
    };
  

    var saveForm = function () {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#tfaa-table tbody").html(data.html_tfaa_list);
            $("#modal-tfaa").modal("hide");
          }
          else {
            $("#modal-tfaa .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };

    /* Binding */
    // Create book
    $(".js-create-book").click(loadForm);
    $("#modal-book").on("submit", ".js-book-create-form", saveForm);
    
    // Update book
    $("#tfaa-table").on("click", ".js-update-tfaa", loadForm);
    $("#modal-tfaa").on("submit", ".js-tfaa-update-form", saveForm);
  
    
    
  

 
    // Delete book
    $("#book-table").on("click", ".js-delete-book", loadForm);
    $("#modal-book").on("submit", ".js-book-delete-form", saveForm);

  });