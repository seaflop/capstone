import file_management as fm
import tts
import ocr

if __name__ == "__main__":
    print("EXECUTING MAIN BLOCK")
    fm.init_folders()
    ocr.resize_image(fm.image_path)
    ocr.ocr(fm.image_path)

    with open(fm.ocr_path, "r") as f:
        file_contents = f.read()
    
    tts.TTS_to_file(file_contents)
    tts.play_audio(fm.tts_path)