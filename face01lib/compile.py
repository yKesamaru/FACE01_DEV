"""License for the Code.

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.
"""


# from setuptools import setup
# from Cython.Build import cythonize
# import glob


# py_file_list = glob.glob('/home/terms/bin/FACE01/face01lib/pyx/*pyx')
# for pyfile in py_file_list:
#     setup(
#         ext_modules = cythonize(
#             pyfile,
#         )
#     )

# setup(
#     ext_modules = cythonize(
#         "Core.pyx",
#     )
# )

# setup(
#     ext_modules = cythonize(
#         "return_face_image.py",
#     )
# )

import os
# os.chdir("/home/terms/bin/FACE01/face01lib/pyx/")

# compile.py
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Compiler import Options


# [Compiler options](https://cython.readthedocs.io/en/stable/src/userguide/source_files_and_compilation.html#compiler-options)
Options.docstrings = True
Options.annotate = False
Options.gcc_branch_hints = True
Options.buffer_max_dims = 4

# [Specify C++ language in setup.py](https://cython.readthedocs.io/en/stable/src/userguide/wrapping_CPlusPlus.html?highlight=language#specify-c-language-in-setup-py)
extensions = [
    # Extension("*", ["*.py"],  # If use glob.
    Extension(
        "*",
        ["*.pyx"],
        # extra_compile_args=['-O3'],  # If you want.
        # language="c++"  # If you want.
    )
]
setup(
    ext_modules = cythonize(
        # [Cythonize arguments](https://cython.readthedocs.io/en/stable/src/userguide/source_files_and_compilation.html#cythonize-arguments)
        extensions,
        nthreads=4,
        compiler_directives= \
        {
            # [Compiler directives](https://cython.readthedocs.io/en/stable/src/userguide/source_files_and_compilation.html#compiler-directives)
            # 'boundscheck': False,  # Default is True.
            # 'wraparound': False,  # Default is True.
            'overflowcheck': True,  # Default is False.True に設定すると、オーバーフローする C 整数算術演算でエラーが発生します。適度なランタイム ペナルティが発生しますが、Python int を使用するよりもはるかに高速です。デフォルトは偽です。
            'cdivision': True,  # Default is False.False に設定すると、Cython は剰余演算子と商演算子の C 型を Python の int 型と一致するように調整し (オペランドの符号が逆の場合は異なります)、右側のオペランドが 0 の場合は ZeroDivisionError を発生させます。これは最大 35% の速度です。ペナルティ。 True に設定すると、チェックは実行されません。 CEP 516 を参照してください。デフォルトは False です。
            # 'profile': True,  # Default is False.Python プロファイラーのフックをコンパイル済みの C コードに書き込みます。デフォルトは偽です。
            'infer_types': True,  # Default is None.関数本体の型指定されていない変数の型を推測します。デフォルトは None で、安全な (意味的に変化しない) 推論のみが許可されることを示します。特に、算術式で使用される変数の整数型の推測は (オーバーフローの可能性があるため) 安全ではないと見なされ、明示的に要求する必要があります。
            'language_level': 3,  # Default is not defined. 2/3/3str
            'unraisable_tracebacks': False,  # Default is not defined. 発生できない例外を抑制するときにトレースバックを出力するかどうか。False
        }
    ),
)

"""compile
cd ~/bin/FACE01/face01lib/pyx
python compile.py build_ext --inplace


pactl set-sink-volume @DEFAULT_SINK@ 30%
play -v 0.2 -q /home/terms/done.wav
"""