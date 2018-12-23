$(document).ready(function() {



            $('form').on('submit', function(event) {

                $.ajax({
                    data : {
                        date : $('#date').val()
                    },
                    type : 'POST',
                    url : '/insert'
                })
                .done(function(data) {

                    if (data.error) {
                        $('#errorAlert').text(data.error).show();
                        $('#successAlert').hide();
                    }
                    else {
                        $('#hasil').show();
                        $('#password').val(data.password);
                        $('#email').val(data.email);
                        $('#code').val(data.enc);
                        $('#t').text(data.date);
                        $('#errorAlert').hide();
                        $('#pilih').hide();
                    }

                });

                event.preventDefault();

            });

        });