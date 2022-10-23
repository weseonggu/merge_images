import tkinter.ttk as ttk
from tkinter import *
import tkinter.messagebox as msgbox
from tkinter import filedialog
from PIL import Image
import os

root=Tk()
root.title("")

#파일 추가
def add_file():
    files= filedialog.askopenfilenames(title="이미지 파일을 선택하세요",\
        filetypes=(("PNG파일","*.png"),("모든 파일","*.*"),("JPG파일","*.jpg")),\
        initialdir=r"C:/")
    for file in files:
        list_file.insert(END, file)
'''열어볼 파일 복수게를 선택이 가능하다  filetypes=("PNG파일","*.png"))이러면 
        png파일확장자의 모든 파일을 받는다   *.*은 모든 파일확징지임  
        initialdir="C:/"은 최초에 c:/ 경로를 보여줌
        initialdir=r 이런 식으로 r을 쓰면 탈출문자든 그냥쓰겠다는 의미임 (추천)'''

#선택 삭제
def del_file():
    #print(list_file.curselection())
    if len(list_file.curselection())==0:
        msgbox.showwarning("경고", "삭제할 이미지를 선택하세요")
        return
    else:
        for index in reversed(list_file.curselection()):
            list_file.delete(index)

'''reversed를 하면 실제 값에는 영향이 없고 바뀌값을 세로운 변수에 저장한다 여기서 그변수는 index임'''

#저장 경로(폴더)
def browsw_dest_path():
    folder_selected=filedialog.askdirectory()
    if folder_selected == '':#사용자가 취소룰 누를때
        return
    txt_dest_path.delete(0,END)#밑에서 Entry가 아닌 Text로하였으면 (1.0,END) 라적어야힘
    txt_dest_path.insert(0,folder_selected)
#파일명 처리 
def file_name_write():
    fileName=file_name_path.get()
    return fileName
    

#이미지 통합
def merge_image():
    # print("가로넓이:",cmd_width.get())
    # print("간격:",cmd_space.get())
    # print("포맷:",cmd_format.get())0

    #가로넓이 
    try:
        img_width=cmd_width.get()
        if img_width == "원본 유지":
            img_width= -1# -1 일떄는 원본유지
        else:
            img_width=int(img_width)

        #간격
        img_space=cmd_space.get()
        if img_space == "좁게":
            img_space= 30
        elif img_space == "보통":
            img_space=60
        elif img_space == "넓게":
            img_space=90
        else:
            img_space=0
        
        #포멧
        img_format=cmd_format.get().lower()# .PNG .JPG .BMP 값을 가지고와서 소문자로 변경
        

        # print(list_file.get(0,END))
        images = [Image.open(x) for x in list_file.get(0,END)]#주소를 가지고와 Image.open으로 이미지를 열고 images애 저장한다
        
        #이미지 사이즈를 리스트에 넣어서 하나씩 처리
        img_sizes=[]#[(width1, height1),(width2, height2),.....] 이런 식으로 저장 한다.
        if img_width > -1:
            #width 값 변경
            img_sizes=[(int(img_width), int(img_width*x.size[1]/x.size[0]))for x in images]
        else:
            #원본사이즈 사용
            img_sizes=[(x.size[0],x.size[1])for x in images]


        #size -> size[0] : width, size[1] : height
        # widths= [x.size[0] for x in images]
        # heights= [x.size[1] for x in images]

        #zip을 이용한 길이 반환
        widths, heights=zip(*(img_sizes))

        # 최대 높이와 전체 높이를 구해옴
        max_width, total_height = max(widths), sum(heights)

        #스케치북 준비
        if img_space >0:#이미지 간격 옵션 적용
            total_height +=(img_space*(len(images)-1))

        result_img=Image.new("RGB",(max_width,total_height),(255,255,255))# 배경흰색
        y_offset=0# 이미지를 붙이고 다음 이미지를 붙일 곳을 계산하는 변수
        # for img in images:
        #     result_img.paste(img, (0,y_offset))
        #     y_offset+=img.size[1]

        for idx, img in enumerate(images):
            #widrh가 원본유자거 아닐떼는 이미지 크기를 조정해야 한다
            if img_width >-1:
                img=img.resize(image_sizes[idx])
            
            result_img.paste(img, (0,y_offset))
            y_offset+=(img.size[1]+img_space)#heiht 값+ 사용자가 지정한 간격

            progress = (idx+1)/ len(images)*100
            p_var.set(progress)
            progress_bar.update()
        

        fn=file_name_write()
        #포맷 옵션 처리
        file_name=fn+"."+img_format
        dest_path = os.path.join(txt_dest_path.get(),file_name)
        result_img.save(dest_path)
        msgbox.showinfo("알림","작업이 완료되었습니다")
    except Exception as err:
        msgbox.showerror("예러",err)

#시작
def start():
    # print("가로넓이:",cmd_width.get())
    # print("간격:",cmd_space.get())
    # print("포맷:",cmd_format.get())
    #파일 먹럭 확인
    if list_file.size() ==0:
        msgbox.showwarning("경고", "이미지 파일을 추가하세요")
        return
    #저장 경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고", "저장경로를 선택하세요")
        return

    #이미지 통합 작업
    file_name_write()
    merge_image()


#파일 프레임
file_frame=Frame(root)
file_frame.pack(fill="x", padx=5, pady=5)

btn_add_file=Button(file_frame, padx=5, pady=5, width=12, text="파일 추가",command=add_file)
btn_add_file.pack(side="left")

btn_del_file=Button(file_frame, padx=5, pady=5, width=12, text="선택 삭제", command=del_file)
btn_del_file.pack(side="right")

#리스트 프레임
list_frame= Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar=Scrollbar(list_frame)
scrollbar.pack(side="right",fill="y")

list_file=Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left",fill="both", expand=True)
scrollbar.config(command=list_file.yview)





#저장경로 프레임
path_frame=LabelFrame(root, text="저장 경로")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_path=Entry(path_frame)
txt_dest_path.pack(side="left",fill="x", expand=True, padx=5, pady=5, ipady=4)#높이 변경

btn_dest_path=Button(path_frame, text="찾아보기",width=10,command=browsw_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

#파일명 프레임
name_frame=LabelFrame(root, text="파일명")
name_frame.pack(fill="x",padx=5, pady=5, ipady=5)

file_name_path= Entry(name_frame)
file_name_path.pack(side="left",fill="x", expand=True, padx=5, pady=5, ipady=4)

#옵션 프레임 
frame_option= LabelFrame(root,text="옵션")
frame_option.pack(padx=5, pady=5, ipady=5)

#1. 가로 넓이 옵션 
#가로 넓이 레이블 
ldl_width=Label(frame_option, text="가로 넓이", width=8)
ldl_width.pack(side="left", padx=5, pady=5)
#가로 넓이 콤보 
opt_width=["원본 유지", "1024", "800", "640"]
cmd_width= ttk.Combobox(frame_option,state="readonly", values=opt_width,width=10)
cmd_width.current(0)
cmd_width.pack(side="left", padx=5, pady=5)

#2, 간격 옵션 
#간격옵션 래이블 
ldl_space=Label(frame_option, text="간격", width=8)
ldl_space.pack(side="left", padx=5, pady=5)

#간격 옵션 콤보
opt_space=["없음", "좁게", "보통", "넓게"]
cmd_space= ttk.Combobox(frame_option,state="readonly", values=opt_space,width=10)
cmd_space.current(0)
cmd_space.pack(side="left", padx=5, pady=5)

#3.파일 포맷 옵션
#파일 포맷 옵션 래이블 
ldl_format=Label(frame_option, text="포멧", width=8)
ldl_format.pack(side="left", padx=5, pady=5)

#파일 포멧 옵션 콤보
opt_format=["PNG", "JPG", "BMP"]
cmd_format= ttk.Combobox(frame_option,state="readonly", values=opt_format,width=10)
cmd_format.current(0)
cmd_format.pack(side="left", padx=5, pady=5)

#진행 상황 progress bar
frame_progress=LabelFrame(root, text="진행상황")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var=DoubleVar()
progress_bar=ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

#실행 프레임 
frame_run=Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close=Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start=Button(frame_run,padx=5, pady=5, text="시작", width=12,command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False,False)
root.mainloop()