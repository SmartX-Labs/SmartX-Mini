# 1. Installing LLM on a local NUC PC
![image](https://user-images.githubusercontent.com/30370933/236706415-0f37aa39-529b-463d-956b-37d612434c23.png)

The model to be used in the lab is a 4-bit fine tuning of the LLaMA-based appaca model.

For the 7B version, if you have more than 4GB of RAM, you can also run it on your laptop.

First, we aim to freely install the model locally and run the chatbot

## the installation steps for the model


git clone https://github.com/antimatter15/alpaca.cpp

cd alpaca.cpp

sudo dnf install -y python3-devel python3-setuptools libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel

wget https://github.com/antimatter15/alpaca.cpp/releases/download/81bd894/alpaca-linux.zip

wget https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/resolve/main/ggml-alpaca-7b-q4.bin

make chat


### ! If the "wget" command is not working, you can manually download the model files from the respective pages and then move the downloaded files to the "git folder"

https://github.com/antimatter15/alpaca.cpp/releases/tag/81bd894

https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/blob/main/ggml-alpaca-7b-q4.bin 


## execute
./chat

## During normal operation

If the model installation and execution have been completed successfully, you can use the chat mode locally to interact with the model and ask questions.

<img width="564" alt="스크린샷 2023-05-08 오전 9 03 30" src="https://user-images.githubusercontent.com/30370933/236709206-6bd31985-4fb4-4454-b274-89f751f4860f.png">


