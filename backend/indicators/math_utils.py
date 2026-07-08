import numpy as np

def enforce_writeable_float_array_fast(data) -> np.ndarray:
    """
    যেকোনো ইনপুট ডেটাকে (List, Series বা Array) একটি রাইটেবল (Writable) 
    এবং সুপার-ফাস্ট সি-কন্টিনিউয়াস (C-contiguous) float64 NumPy অ্যারেতে রূপান্তর করে।
    এটি মেমোরি পয়েন্টার হ্যান্ডলিং অপ্টিমাইজ করে লাইভ মার্কেটের গতি বাড়ায়।
    """
    # ১. ইনপুট যদি অলরেডি NumPy অ্যারে না হয়, তবে তাকে float64 অ্যারেতে রূপান্তর করা
    if not isinstance(data, np.ndarray):
        arr = np.array(data, dtype=np.float64)
    else:
        # যদি অলরেডি অ্যারে হয়, তবে মেমোরি কপি না করে সরাসরি float64 ভিউ নেওয়া (যদি সম্ভব হয়)
        arr = data.astype(np.float64, copy=False)
    
    # ২. মেমোরি কন্টিনিউটি (C-Contiguous) এনফোর্স করা (যাতে CPU ক্যাশ মেমোরি ফাস্ট রিড করতে পারে)
    if not arr.flags['C_CONTIGUOUS']:
        arr = np.ascontiguousarray(arr)
        
    # ৩. অ্যারেটি যেন রাইটেবল (Writable) হয় তা নিশ্চিত করা, যাতে পরবর্তী ক্যালকুলেশনে এরর না আসে
    if not arr.flags['WRITEABLE']:
        arr = arr.copy()
        arr.setflags(write=True)
        
    return arr

def calculate_rolling_view(arr: np.ndarray, window: int) -> np.ndarray:
    """
    লুপ ছাড়া অত্যন্ত দ্রুত রোলিং উইন্ডো বা মুভিং উইন্ডো ক্যালকুলেট করার জন্য 
    NumPy-এর স্ট্রাইডস (Strides) মেমোরি ট্রিক ব্যবহার করা।
    """
    arr = enforce_writeable_float_array_fast(arr)
    if len(arr) < window:
        return np.array([], dtype=np.float64)
        
    shape = (arr.size - window + 1, window)
    strides = (arr.strides[0], arr.strides[0])
    return np.lib.stride_tricks.as_strided(arr, shape=shape, strides=strides)
