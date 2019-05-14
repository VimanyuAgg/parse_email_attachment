@echo on
call C:\ProgramData\Anaconda3\condabin\activate.bat "skills_env"
C:\Users\vimanyua\.conda\envs\skills_env\python.exe "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\put_file_in_s3.py" "user_demographic" > "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\print_logs\user_demographic_print_%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.log" 2>&1 %*

MOVE "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\User_Demographics_PS_Consultants_v1_vim_pipeline_report.csv" "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\old_prod_basefiles\Basefile_user_demographic_%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.csv"
MOVE "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\user_demographic_data_cleaned_%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.csv" "C:\Users\vimanyua\PycharmProjects\Pipeline\skills_data\cleaned_basefiles\Cleaned_user_demographic_Basefile_%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.csv"

C:\ProgramData\Anaconda3\condabin\deactivate.bat
pause