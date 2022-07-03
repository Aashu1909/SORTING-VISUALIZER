import pygame
# Importing random module to generate some ramdom array
import random
pygame.init()

class DrawInformation:
    # RGB color list
    BLACK=0,0,0
    WHITE= 255,255,255
    GREEN=0,255,0
    RED=255,0,0
    YELLOW=255,255,0
    GREY=160,160,160
    DARK_GREY=192,192,192
    LIGHT_GREY=128,128,128
    BACKGROUND_COLOR=242, 241, 239
    GRADIANT=[GREY,LIGHT_GREY,DARK_GREY]
    
    SIDE_PAD=100
    TOP_PAD=150

    FONT=pygame.font.SysFont('Monserat',30)
    LARGE_FONT=pygame.font.SysFont('Monserat',50)

    def __init__(self, width, height, lst):
        self.width=width
        self.height=height
        self.window=pygame.display.set_mode((width,height))
        pygame.display.set_caption("SORTING ALGORITHM VISUALIZER")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val= max(lst)
        self.min_val= min(lst)
        
        # Bar wodth and height area
        self.block_width=round((self.width - self.SIDE_PAD) / len(lst) )
        self.block_height=round((self.height - self.TOP_PAD) / (self.max_val-self.min_val) )
        self.start_x=self.SIDE_PAD//2


# implementing a function named draw window which takes the drawinformation class instance as parameter
def draw(draw_info,algorithm_name):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title=draw_info.LARGE_FONT.render(f'{algorithm_name}',1,draw_info.RED)
    draw_info.window.blit(title,(draw_info.width/2-title.get_width()/2, 5))

    sorting=draw_info.FONT.render('B-Bubble Sort | I-Insertion Sort | S-Selection Sort | Q-Quick Sort | H-Heap Sort', 1, draw_info.BLACK)
    draw_info.window.blit(sorting,(draw_info.width/2-sorting.get_width()/2, 65))
    
    controls=draw_info.FONT.render('R-Reset | Space-Start Sotring ',1,draw_info.BLACK)
    draw_info.window.blit(controls,(draw_info.width/2-controls.get_width()/2, 40))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info,color_position={},clear_bg=False):
    lst=draw_info.lst

    if clear_bg:
        clear_rect=(draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                    draw_info.width-draw_info.SIDE_PAD, draw_info.height-draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR,clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + (i * draw_info.block_width)
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIANT[i % 3]

        if i in color_position:
            color=color_position[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

def generate_starting_list(n,min_val,max_val):
    lst=[]
    for _ in range(n):
        val=random.randint(min_val,max_val)
        lst.append(val)
    return lst


def bubble_sort(draw_info):
    lst=draw_info.lst
    for i in range(len(lst)):
        for j in range(len(lst)-i-1):
            num1=lst[j]
            num2=lst[j+1]

            if (num1 > num2):
                lst[j],lst[j+1]=lst[j+1],lst[j]
                draw_list(draw_info,color_position={j:draw_info.GREEN,j+1:draw_info.RED},clear_bg=True)
                yield True
    return lst

def insertion_sort(draw_info):
    lst=draw_info.lst

    for i in range(1, len(lst)):
        key = lst[i]
        j = i-1
        while j >= 0 and key < lst[j] :
                lst[j + 1] = lst[j]
                j -= 1
        lst[j + 1] = key
        draw_list(draw_info,color_position={j-1:draw_info.GREEN,j:draw_info.RED},clear_bg=True)
        yield True
    return lst

def selection_sort(draw_info):
    lst=draw_info.lst
    for i in range(len(lst)):      
        min_idx = i
        for j in range(i+1, len(lst)):
            if lst[min_idx] > lst[j]:
                min_idx = j
        
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info,color_position={min_idx:draw_info.GREEN,i:draw_info.RED},clear_bg=True)
        yield True
    return lst

def partition(arr, l, h):
    i = ( l - 1 )
    x = arr[h]
  
    for j in range(l, h):
        if   arr[j] <= x:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
  
    arr[i + 1], arr[h] = arr[h], arr[i + 1]
    
    return (i + 1)
  
def quickSortIterative(draw_info):  
    lst=draw_info.lst
    size =len(lst)
    stack = [0] * (size)
    l=0
    h=size-1
    # initialize top of stack
    top = -1
  
    # push initial values of l and h to stack
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h
    while top >= 0:
        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1
  
        p = partition(lst, l, h)

        if p-1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1
  
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h
        draw_list(draw_info,color_position={p:draw_info.GREEN, h:draw_info.RED},clear_bg=True)
        yield True
    return lst

def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
  
    # See if left child of root exists and is
    # greater than root
    if l < n and arr[largest] < arr[l]:
        largest = l
  
    # See if right child of root exists and is
    # greater than root
    if r < n and arr[largest] < arr[r]:
        largest = r
  
    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        # Heapify the root.
        heapify(arr, n, largest)

def heapSort(draw_info):
    arr=draw_info.lst
    n = len(arr)
  
    # Build a maxheap.
    for i in range(n//2 - 1, -1, -1):
        # draw_list(draw_info,color_position={i:draw_info.RED},clear_bg=True)
        # yield True
        heapify(arr, n, i)
        draw_list(draw_info,color_position={i:draw_info.YELLOW},clear_bg=True)
        yield True
  
    # One by one extract elements
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)
        draw_list(draw_info,color_position={i:draw_info.GREEN},clear_bg=True)
        yield True
        

def main():
    WIDTH=800
    HEIGHT=600

    run=True
    # To regulate how quickly this loop will run
    clock=pygame.time.Clock()
    
    n=50
    min_val=10
    max_val=100
    lst=generate_starting_list(n,min_val,max_val)
    print(lst)
    draw_info=DrawInformation(WIDTH, HEIGHT, lst)
    
    sorting =False

    sorting_algorithm=None
    sorting_algo_name=None
    sorting_algorithm_generator=None

    while run:
        # To be run at 60 fps
        clock.tick(40)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting=False
        else:
            draw(draw_info,sorting_algo_name)
        for event in pygame.event.get():
            # Sorting controls 
            if event.type==pygame.QUIT:
                run=False

            if event.type!=pygame.KEYDOWN:
                # That means if any preses down on keybord
                continue
            if event.key == pygame.K_r:
                # When r is pressed we reset the sorting visualizser
                lst=generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting=False

            if event.key == pygame.K_SPACE and sorting==False:
                sorting=True            
                sorting_algorithm_generator=sorting_algorithm(draw_info)
            elif event.key == pygame.K_b and sorting==False:
                sorting_algorithm=bubble_sort
                sorting_algo_name='Bubble Sort'
            elif event.key == pygame.K_i and sorting==False:
                sorting_algorithm=insertion_sort
                sorting_algo_name='Insertion Sort'
            elif event.key == pygame.K_s and sorting==False:
                sorting_algorithm=selection_sort
                sorting_algo_name='Selection Sort'
            elif event.key == pygame.K_q and sorting==False:
                sorting_algorithm=quickSortIterative
                sorting_algo_name='Quick Sort'
            elif event.key == pygame.K_h and sorting==False:
                sorting_algorithm=heapSort
                sorting_algo_name='Heap Sort'
            


    pygame.quit()

if __name__=='__main__':
    main()