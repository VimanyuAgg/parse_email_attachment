@echo on
call C:\ProgramData\Anaconda3\condabin\activate.bat "skills_env"
C:\Users\vimanyua\.conda\envs\skills_env\python.exe "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\put_file_in_s3.py" > "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\print_logs\%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.log" 2>&1 %*

MOVE "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\Skills_Data_vim_pipeline_report.csv" "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\old_prod_basefiles\Basefile_%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.csv"
MOVE "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\skills_data_cleaned_%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.csv" "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\cleaned_basefiles\Cleaned_Basefile_%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.csv"

C:\ProgramData\Anaconda3\condabin\deactivate.bat
pause