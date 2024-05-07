# Persistent Memory Bot
## V.1.0 Is available here. v.2.0 Is coming soon! Still in development. Release date Summer 2025
planned features:
-smart memory
-topic creation
-queues
A chatbot that can remember all previous conversations.
### v1.5 changelog:
Useful for any application that requires an locally running chatbot. (No LM Studio needed!) functions
with a persistent memory.
### v.1
Useful for any application that requires an LM studio chatbot and functions identically to a traditional python call of a local AI Application.
## TO INSTALL:
```
Pip install flask install 
Pip3 install huggingface-hub
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python

```
## Full docs:
```
# Base ctransformers with no GPU acceleration
pip install llama-cpp-python
# With NVidia CUDA acceleration
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
# Or with OpenBLAS acceleration
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
# Or with CLBLast acceleration
CMAKE_ARGS="-DLLAMA_CLBLAST=on" pip install llama-cpp-python
# Or with AMD ROCm GPU acceleration (Linux only)
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" pip install llama-cpp-python
# Or with Metal GPU acceleration for macOS systems only
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

# In windows, to set the variables CMAKE_ARGS in PowerShell, follow this format; eg for NVidia CUDA:
$env:CMAKE_ARGS = "-DLLAMA_OPENBLAS=on"
pip install llama-cpp-python

huggingface-cli download TheBloke/Silicon-Maid-7B-GGUF silicon-maid-7b.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False

huggingface-cli download lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF  Meta-Llama-3-8B-Instruct-Q8_0.gguf --local-dir . --local-dir-use-symlinks False


```
