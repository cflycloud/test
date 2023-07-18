import subprocess
import os


class CodeCompiler:
    def __init__(self, c_file, output_dir):
        self.c_file = c_file
        self.output_dir = output_dir
        self.output_file = os.path.join(output_dir, "../test.exe")

    def compile(self):
        os.makedirs(self.output_dir, exist_ok=True)
        compile_command = "gcc -o {} {}".format(self.output_file, self.c_file)

        try:
            compile_output = subprocess.check_output(compile_command, stderr=subprocess.STDOUT, shell=True)
            compile_str = compile_output.decode() + "\nCompile done ...\n\n"
        except subprocess.CalledProcessError as e:
            compile_output = e.output
            compile_str = "Compile Error: " + compile_output.decode() + "\n\n"

        print(compile_output.decode())
        return compile_str

    def run(self):
        if os.path.isfile(self.output_file):
            run_command = self.output_file
            try:
                run_output = subprocess.check_output(run_command, stderr=subprocess.STDOUT, shell=True)
                run_str = run_output.decode() + "\nProcess finished with exit code 0\n\n"
                print("Process finished with exit code 0")
            except subprocess.CalledProcessError as e:
                run_output = e.output
                run_str = "Run Error: " + run_output.decode() + "\n\n"
            print(run_output.decode())
        return run_str