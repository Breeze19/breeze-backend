$(document).ready(function(){
  $("#sportsDropdown").on('change',function(){
    var val = $("#sportsDropdown :selected").val()
    if(val == 'tkk'){
      window.location = '/sports/tkk/'
    } else if(val == 'tkp'){
      window.location = '/sports/tkp/'
    }
  })
  $("#submit").on('click',function(){
    $("#loader1").removeAttr('hidden')
    const data = {
      sportsName: $("#sportsDropdown :selected").text(),
      noofplayers: $("#noofplayers").val(),
      name: $("#name").val(),
      collegeName: $("#collegeName").val(),
      email: $("#email").val(),
      phno: $("#phno").val(),
      req_acc:  $("#accomoDown :selected").text()
    }
    console.log(data)
    $.post("https://breeze19sports.herokuapp.com/register",{data},function(response){
      console.log(response)
      $("#loader1").attr('hidden',true)
      if(response.result == 'OK'){
        $("#message").removeAttr('hidden')
        $("#message").text("Registration successful")
      } 
      else{
        $("#message").attr('hidden')
        $("#message").text("Please try again")
      }
    })
  })
  $("#submittkk").on('click',function(){
    $("#loader1").removeAttr('hidden')
    const data = {
      weightCatBoys: $("#weightCatBoys :selected").text(),
      weightCatGirls: $("#weightCatGirls :selected").text(),
      category: $("#category :selected").text(),
      name: $("#name").val(),
      collegeName: $("#collegeName").val(),
      email: $("#email").val(),
      phno: $("#phno").val(),
      req_acc:  $("#accomoDown :selected").text()
    }
    $.post("https://breeze19sports.herokuapp.com/register/tkk",{data},function(response){
    $("#loader1").attr('hidden',true)
      if(response.result == 'OK'){
        $("#message").removeAttr('hidden')
        $("#message").text("Registration successful")
      } 
      else{
        $("#message").attr('hidden')
        $("#message").text("Please try again")
      }
    })
  })
  $("#submittkp").on('click',function(){
    $("#loader1").removeAttr('hidden')
    const data = {
      category1: $("#category1 :selected").text(),
      category2:$("category2 :selected").text(),
      belt: $("#belt").text(),
      noofplayers: $("#noofplayers").val(),
      name: $("#name").val(),
      collegeName: $("#collegeName").val(),
      email: $("#email").val(),
      phno: $("#phno").val(),
      req_acc:  $("#accomoDown :selected").text()
    }
    $.post("https://breeze19sports.herokuapp.com/register/tkp",{data},function(response){
      $("#loader1").attr('hidden',true)
      if(response.result == 'OK'){
        $("#message").removeAttr('hidden')
        $("#message").text("Registration successful")
      }
      else{
        $("#message").attr('hidden')
        $("#message").text("Please try again")
      }
    })
  })
})
