import $ from 'jquery';
import 'select2';
import 'select2/dist/css/select2.min.css';
import 'select2/dist/js/select2.full.min.js';

$(document).ready(function () {
  $('#id_comic').select2({
    closeOnSelect: true,
    placeholder: 'Select a comic',
    multiple: false,
    amdLanguageBase: 'select2/i18n/',

  });
  // when user clicks add more btn of images
  $(".add-images").click(function (ev) {
    ev.preventDefault();
    const count = $("#item-images").children().length;
    const tmplMarkup = $("#images-template").html() as string;
    const compiledTmpl = tmplMarkup.replace(/__prefix__/g, count.toString());
    $("#item-images").append(compiledTmpl);

    // update form count
    $("#id_images-TOTAL_FORMS").attr("value", (count + 1).toString());
  });
});
