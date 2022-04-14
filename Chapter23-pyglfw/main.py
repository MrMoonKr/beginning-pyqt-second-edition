

import glfw

curr_time = 0
prev_time = 0
frame_count = 0


def update():
    pass
    #print( "update() 호출됨" )
    #curr_time = glfw.get_time()
    #print( f"현재시간 : {curr_time}" )

def render():
    pass
    #print( "render() 호출됨" )


def main():
    print( "main() 호출됨" )

    if not glfw.init():
        raise Exception("glfw can not be initialized !!!")

    window = glfw.create_window( 640, 480, "GLFW 윈도우", None, None )
    if not window:
        glfw.terminate()
        raise Exception( "[glfw] 윈도우 생성 실패" )
    
    glfw.make_context_current( window )
    glfw.swap_interval( 0 )

    curr_time   = glfw.get_time()
    prev_time   = curr_time
    frame_count = 0
    frame_time  = curr_time
    while not glfw.window_should_close( window ):
        #
        frame_count += 1
        curr_time = glfw.get_time()
        delt_time = curr_time - prev_time
        prev_time = curr_time
        #print( f"경과시간 : {delt_time}" )
        
        if curr_time - frame_time >= 1.0:
            #print( f"FPS : {frame_count}" )
            glfw.set_window_title( window, f"FPS : {frame_count}" )
            frame_count = 0
            frame_time  = curr_time

        update()

        #
        render()

        #
        glfw.swap_buffers( window )
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()

