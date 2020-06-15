--[[
    New state class to model the required paused state
]]
PauseState = Class{__includes = BaseState}

--[[
    Need to save the different parameters from the previous playing state
    and the paused icon is loaded
]]
function PauseState:enter(params)
    self.saved = params
    self.image = love.graphics.newImage('pause.png')
end


function PauseState:update(dt)

    -- go back to play if enter is pressed
    if love.keyboard.wasPressed('p') then
        -- updating the music
        sounds['pause']:play()
        sounds['music']:resume()
        -- allow update of scrolling background
        gScroll = true
        gStateMachine:change('play',self.saved)
    end
end

--[[
    The previous info from the playing state is printed along with the pause icon
]]
function PauseState:render(dt)

    for k, pair in pairs(self.saved.pipePairs) do
        pair:render()
    end

    love.graphics.setFont(flappyFont)
    love.graphics.print('Score: ' .. tostring(self.saved.score), 8, 8)

    self.saved.bird:render()
    love.graphics.draw(self.image, VIRTUAL_WIDTH/2-80, VIRTUAL_HEIGHT/2-100,0,0.5,0.5,0,0)
    
end