(function () {
  var $ChatInput;
  $ChatInput = $('.ChatInput-input');

  $ChatInput.keyup(function (e) {
    var $this, newText;
    // if (e.shiftKey && e.which === 13) {
    //   e.preventDefault();
    //   return false;
    // }
    $this = $(this);
    if (e.which === 13) {
      newText = $(this).text();
      // newText = newText.replace(/<div><br><\/div>/g, '');
      // newText = newText.replace(/&nbsp;/g, '');
      var sendData = newText.replace(/\s+/g, ' ');
      var dataList = sendData.split(" ");
      var checkLenText = [];
      $.each(dataList, function (index, word) {
        var regexSC1 = /[A-Za-z0-9]*.*[\W_]+[A-Za-z0-9]+/;
        var regexSC2 = /[A-Za-z0-9]+.*[\W_]+[A-Za-z0-9]*/;
        var regexWN = /^[A-Za-z0-9]+$/;
        if (regexSC1.test(word) || regexSC2.test(word) || regexWN.test(word)) {
          checkLenText.push(word);
        }
      });

      // console.log("newText.length = ", newText.length);
      // console.log("newText = ", newText + ";");
      // console.log("sendData.length = ", sendData.length);
      // console.log("sendData = ", sendData + ";");
      // console.log("checkLenText.length = ", checkLenText.length);
      // console.log("checkLenText = ", checkLenText);

      if (checkLenText.length > 1) {
        $this.html('');
        // Adding ques in chat
        $('.ChatWindow').append('<div class="ChatItem ChatItem--expert"> <div class="ChatItem-meta"> <div class="ChatItem-avatar"> <img class="ChatItem-avatarImage" src="../../static/user/img/profile.jpg"> </div> </div> <div class="ChatItem-chatContent"> <div class="ChatItem-chatText">' + newText + '</div> </div> </div>');
        // making chat loading screen visible
        $('.ChatLoading').css('display', 'block');
        // Scroll to bottom after adding ques
        $('.ChatWindow').animate({
          scrollTop: $('.ChatWindow').prop("scrollHeight")
        }, 500);

        $.ajax({
          url: '/user/send_answer/',
          data: {
            'question': sendData,
          },
          dataType: 'json',
          success: function (returnData) {
            // Adding ans in chat
            $('.ChatWindow').append(`
      <div class="ChatItem ChatItem--expert-AI">
        <div class="ChatItem-meta-AI">
            <div class="ChatItem-avatar-AI"> <img class="ChatItem-avatarImage-AI"
                    src="../../static/user/img/askAI.png">
            </div>
        </div>
        <div class="ChatItem-chatContent-AI">
            <div class="ChatItem-chatText-AI"> 
            `+ returnData.answer +`
            </div>
            <div class="refBtn" onclick="showDiv(this)">Show Reference</div>
            <div class="ChatItem-chatdetails-AI">
                <div>
                <span style="color: rgb(180, 180, 180); font-weight:700">Source:&nbsp;</span>
                    `+ returnData.source +`
                </div>
                <div>
                <span style="color: rgb(180, 180, 180); font-weight:700">Page No:&nbsp;</span>
                    `+ returnData.page +`
                </div>
                <div>
                <span style="color: rgb(180, 180, 180); font-weight:700">Line:&nbsp;</span>
                    `+ returnData.line +`
                </div>
            </div>
        </div>
      </div>`);
            // making chat loading screen disappear 
            $('.ChatLoading').css('display', 'none');
            // Scroll to bottom after adding ans
            return $('.ChatWindow').animate({
              scrollTop: $('.ChatWindow').prop("scrollHeight")
            }, 500);
          },
          error: function (error) {
            console.log(error);
          }
        });
      }
      else {
        if (checkLenText.length == 0) {
          e.preventDefault();
          swal({
            title: "Warning",
            text: "You can't submit empty question or question containing only special characters!",
            icon: "warning",
          });
          return false;

        }
        else {
          e.preventDefault();
          swal({
            title: "Warning",
            text: "You can't submit less than 2 words question!",
            icon: "warning",
          });
          return false;

        }
      }
    }
  });

}).call(this);

// show reference
function showDiv(button) {
  var parent = button.parentElement;
  var div = parent.querySelector(".ChatItem-chatdetails-AI");
  
  var parentJQ = $(button).parent();
  var divJQ = parentJQ.find(".ChatItem-chatdetails-AI");
  if(div){
    if (div.style.display === 'block') {
      // div.style.display = 'none';
      divJQ.slideUp('slow');
    }
    else{
      // div.style.display = 'block';
      divJQ.slideDown('slow');
      // Scroll to bottom after clicking show ref
      $('.ChatWindow').animate({
        scrollTop: $('.ChatWindow').prop("scrollHeight")
      }, 500);
    }
  }
}

// Scroll to bottom after reloading
$('.ChatWindow').animate({
  scrollTop: $('.ChatWindow').prop("scrollHeight")
}, 500);