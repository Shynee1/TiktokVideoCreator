import requests, base64, json, threading

ENDPOINT = 'https://tiktok-tts.weilnet.workers.dev'
TEXT_LIMIT = 300

class TikTokTTS:
    def __init__(self, voice: str):
        self.voice = voice

    # Split a large chunk of text into short pieces
    def split_text(self, text: str, max_size: int) -> list[str]:
        sentence_delimiters = ['.', '?', '!']
        
        split_strs = []
        curr_str = ""
        for character in text:  
            # Split into sentences
            if character in sentence_delimiters:
                if curr_str != "":
                    split_strs.append((curr_str + character).strip())
                curr_str = ""
            # Split if current sentence is over character limit
            elif len(curr_str) + 1 >= max_size:
                # Save last word and store overflow for next chunk
                last_word_index = curr_str.rfind(" ") + 1
                resized_str = curr_str[:last_word_index]
                overflow = curr_str[last_word_index]
                split_strs.append(resized_str.strip())
                curr_str = overflow + character
            else:
                curr_str += character
        
        split_strs.append(curr_str)
        return split_strs

    # Test whether the endpoint is still functioning      
    def endpoint_active(self) -> bool:
        response = requests.get(ENDPOINT)
        return response.status_code == 200
    
    # Send POST request to TikTok TTS and parse into base64 encoded string
    def generate_audio(self, text: str) -> str:
        url = ENDPOINT + "/api/generation"
        headers = {'Content-Type': 'application/json'}
        data = {'text': text, 'voice': self.voice}
        response = requests.post(url, headers=headers, json=data) 
        return json.loads(response.content)["data"]

    # Decode base64 string and save to file
    def save_audio(self, audio: str, path: str):
        filename = path
        audio_data = base64.b64decode(audio)
        with open(filename, "wb") as file:
            file.write(audio_data)

    # Use multi-threading to generate audio for each split string
    def thread_audio(self, split_text):
        base64_data = [""] * len(split_text)

        # Generate TTS for every chunk and store in list
        def thread_function(index, text):
            b64_string = self.generate_audio(text)
            base64_data[index] = b64_string

        threads = []
        for i in range(len(split_text)):
            thread = threading.Thread(target=thread_function, args=(i, split_text[i]))
            thread.start()
            threads.append(thread)
            # Wait for all threads to finish executing
            thread.join()

        # Join all base64 fragments into one string
        return "".join(base64_data)

    def create_tts(self, text: str, path: str):
        if not self.endpoint_active():
            print("ERROR: TTS service is not active")
            return

        split_text = self.split_text(text, TEXT_LIMIT)
        audio_str = self.thread_audio(split_text)

        self.save_audio(audio_str, path)
        print("Successfully saved audio to " + path)
        
