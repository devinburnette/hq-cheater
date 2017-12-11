$(document).ready(function() {
                $("#searchbox").keypress(function(event) {
                        if (event.which == 13) {
                                event.preventDefault();
                                search();
                        }
                });
                $("#rec").click(function(event) {
                        switchRecognition();
                });
        });
        var recognition;
        function startRecognition() {
                recognition = new webkitSpeechRecognition();
                recognition.onstart = function(event) {
                        updateRec();
                };
                recognition.onresult = function(event) {
                        var text = "";
                    for (var i = event.resultIndex; i < event.results.length; ++i) {
                        text += event.results[i][0].transcript;
                    }
                    setInput(text);
                        stopRecognition();
                };
                recognition.onend = function() {
                        stopRecognition();
                };
                recognition.lang = "en-US";
                recognition.start();
        }

        function stopRecognition() {
                if (recognition) {
                        recognition.stop();
                        recognition = null;
                }
                updateRec();
        }
        function switchRecognition() {
                if (recognition) {
                        stopRecognition();
                } else {
                        startRecognition();
                }
        }
        function setInput(text) {
                $("#searchbox").val(text);
                search();
        }
        function updateRec() {
                $("#rec").text(recognition ? "Stop" : "Speak");
        }

