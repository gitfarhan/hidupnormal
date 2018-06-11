$(document).ready(function() {

            $('form').on('submit', function(event) {

                $.ajax({
                    data : {
                        KodeInput : $('#KodeInput').val()
                    },
                    type : 'POST',
                    url : '/process'
                })
                .done(function(data) {

                    if (data.total) {
                        $('#notfinished').show();
                        $('#total').text(data.total);
                        $('#finished').hide();
                    }
                    if(data.password) {
                        $('#finished').show();
                        $('#password').val(data.password);
                        $('#notfinished').hide();
                    }

                    if (data.error) {
                        $('#finished').show();
                        $('#password').val(data.form);
                        $('#notfinished').hide();
                    }

                });

                event.preventDefault();

            });

        });