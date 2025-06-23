local draggables, player do
    player = {}
    player.menu_open = true
    draggables = {}
    draggables.mouse_button_left = false
    draggables.DPI = 1
    draggables.data = {}
    draggables.current = nil
    local moving = false
    local dpi_ref = gui.ctx:find('misc>menu>dpi scale')

    dpi_ref:add_callback(function() 
        local raw_value = dpi_ref:get_value():get():get_raw()
        local dpi_mapping = {
            [2] = 0.5,
            [4] = 0.75,
            [8] = 1,
            [16] = 1.25,
            [32] = 1.5,
            [64] = 2
        }
        draggables.DPI = dpi_mapping[raw_value] or 1
    end)

    draggables.in_bounds = function(vec1, vec2)
        local mouse_x, mouse_y = gui.input:cursor().x * draggables.DPI, gui.input:cursor().y * draggables.DPI
        return mouse_x >= vec1.x and mouse_x <= vec2.x and mouse_y >= vec1.y and mouse_y <= vec2.y
    end

    --  is_dragging function
    draggables.is_dragging = function()
        return draggables.moving
    end

    draggables.create = function(id, default_x, default_y, w, h, only_y)
        only_y = only_y or false
        local mouse_x, mouse_y = gui.input:cursor().x * draggables.DPI, gui.input:cursor().y * draggables.DPI

        if not draggables.data[id] then
            draggables.data[id] = {
                x = default_x,
                y = default_y,
                position = draw.vec2(0, 0),
                state = false,
                moving = false
            }
        end

        local drag_x, drag_y = draggables.data[id].x, draggables.data[id].y
        local screen_x, screen_y = game.engine:get_screen_size()

        if draggables.in_bounds(draw.vec2(drag_x, drag_y), draw.vec2(drag_x + w, drag_y + h)) and 
           draggables.in_bounds(draw.vec2(0, 0), draw.vec2(screen_x, screen_y)) then
            if draggables.mouse_button_left and player.menu_open and not draggables.data[id].state and 
               (draggables.current == nil or draggables.current == id) then
                draggables.moving = true
                moving = true
                draggables.data[id].state = true
                draggables.data[id].moving = true
                draggables.current = id
                draggables.data[id].position = draw.vec2(drag_x - mouse_x, drag_y - mouse_y)
            end
        end

        if not draggables.mouse_button_left then
            draggables.data[id].state = false
            draggables.current = nil
            moving = false
            draggables.data[id].moving = false
        end

        if draggables.data[id].state then
            if only_y then
                draggables.data[id].y = mouse_y + draggables.data[id].position.y
            else
                draggables.data[id].x = mouse_x + draggables.data[id].position.x
                draggables.data[id].y = mouse_y + draggables.data[id].position.y
            end
        end
    end

    local INSERT_KEY = 0x2D 
    local DELETE_KEY = 0x2E

    events.input:add(function(msg, w, l)
        if msg == 0x0201 then 
            draggables.mouse_button_left = true
        elseif msg == 0x0202 then
            draggables.mouse_button_left = false
        end
        if w == INSERT_KEY or w == DELETE_KEY then
            player.menu_open = not player.menu_open
        end
    end)

    events.create_move:add(function(cmd)
        if moving then
            cmd:remove_button(input_bit_mask.in_attack)
        end
    end)
end
