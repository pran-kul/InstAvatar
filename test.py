import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

# CUDA kernel function
mod = SourceModule("""
__global__ void hello_cuda() {
    printf("Hello CUDA!\\n");
}
""")

# Get kernel function
hello_cuda = mod.get_function("hello_cuda")

# Run CUDA kernel
hello_cuda(block=(1, 1, 1), grid=(1, 1))

