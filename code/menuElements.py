
from utils import *
import pygame
import math
import random
from gui import *
from pygame.locals import *


class Panel(object):
    """Panel(mouse, rect) -> new Panel. 
    The basic building block of the menu system. """
    color = BS1
    image = None
    drawBorder = True
    bgColor = None
    def __init__(self, rect, corners = []):
        self.rect = rect
        self.panels = []
        self.corners = corners
    
    def update(self):
        """updates this panel and its children"""
        for panel in self.panels:
            panel.update()
            
    def addPanel(self, panel):
        """adds a subpanel to this panel."""
        self.panels.append(panel)
    
    def removePanel(self, panel):
        """removes a subpanel from this panel."""
        if self.panels.count(panel):
            self.panels.remove(panel)
    
    def reset(self):
        for panel in self.panels:
            panel.reset()
    
    def click(self, button, pos):
        """called when this panel is clicked on."""
        #pass the click on to first colliding child:
        for panel in self.panels:
            if panel.rect.collidepoint(pos):
                if panel.click(button, pos):
                    return True
    
    def move(self, pos, rel):
        """called when the mouse moves to or from this panel."""
        oldpos = pos[0] - rel[0] , pos[1] - rel[1]
        for panel in self.panels:
            if panel.rect.collidepoint(oldpos) or panel.rect.collidepoint(pos):
                panel.move(pos, rel)
                
    def dragOver(self, pos, rel):
        """called when the mouse moves to or from this panel."""
        oldpos = pos[0] - rel[0] , pos[1] - rel[1]
        for panel in self.panels:
            if panel.rect.collidepoint(oldpos) or panel.rect.collidepoint(pos):
                panel.dragOver(pos, rel)
        
    def drag(self, start):
        """drag(start): 
        The mouse has started dragging at start.  This should be passed down to
        any colliding subpanels.  If all subpanels return None, this should 
        return None if self is not draggable, and return (self, self.parent) 
        if self is draggable."""
        for panel in self.panels:
            if panel.rect.collidepoint(start):
                dragged = panel.drag(start)
                if dragged:
                    return dragged
        return None
        
    def drop(self, pos, dropped):
        """drop(pos, dropped): 
        The dragged object was dropped on this panel at pos.
        This should be passed down to any colliding subpanels.  If all 
        subpanels return None, this should return None if the dropped
        object has no effect here, 1 if the object should be moved here,
        2 if the object should exist here and at the source, or another 
        non-zero, non-None value for special cases. 
        Use is:
            dragged = source.drag(mousePos)
            ...
            source.endDrag(target.drop(mousePos2, dragged), dragged)"""
        for panel in self.panels:
            if panel.rect.collidepoint(pos):
                result = panel.drop(pos, dropped)
                if result:
                    return result
    
    def endDrag(self, dragged, result):
        """called when a drag from here drops with a non-None result."""
        if result == 1:
            self.removePanel(dragged)
    
    def draw(self, surface, rect):
        """draws this panel on the surface."""
        if rect:
            rect = rect.clip(self.rect)
        else:
            rect = self.rect
        if self.bgColor:
            pygame.draw.rect(surface, self.bgColor, rect, 0)
        
        if self.image:
            surface.blit(self.image, (rect.left, rect.top), (0, 0, rect.width, rect.height))
       
        for panel in self.panels:
            panel.draw(surface, rect)
        if self.drawBorder:
            diamondRect(surface, self.color, rect, self.corners)   

    def handleEvent(self, keys):
        for panel in self.panels:
            panel.handleKeys(keys)


class TopLevelPanel(Panel):
    """ TopLevelPanel(rect) -> TopLevelPanel.
    Like a panel, but has a handleEvent() method and draws subpanels to a 
    buffer.  Must be the ultimate parent of any panel that responds to events,
    and events should all be passed to .handleEvent(event)."""
    bgColor = 15,31,78
    dragged = None
    dragSource = None
    internalPos = None
    def __init__(self, rect, corners = []):
        Panel.__init__(self, rect, corners)
        self.image = pygame.Surface(rect.size, \
                            flags = (hardwareFlag)).convert()
        self.image.set_alpha(200)
                            
    def handleEvent(self, event):
        """Examines the event and passes it down to children as appropriate."""
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.internalPos = event.pos[0] - self.rect.left, \
                            event.pos[1] - self.rect.top
            self.click(event.button, self.internalPos)
            
        elif event.type == pygame.MOUSEBUTTONUP:
            self.internalPos = event.pos[0] - self.rect.left, \
                            event.pos[1] - self.rect.top
            if self.dragged:
                if self.dragged != 1:
                    self.dragSource.endDrag(self.dragged, \
                                self.drop(self.internalPos,	self.dragged))
                self.dragged = None
                self.dragSource = None
                
        elif event.type == pygame.MOUSEMOTION:
            self.internalPos = event.pos[0] - self.rect.left, \
                            event.pos[1] - self.rect.top
            if event.buttons[0]:#dragging disabled for now.
                if not self.dragged:
                    self.dragged = self.drag(self.internalPos)
                    if self.dragged: 
                        self.dragged, self.dragSource = self.dragged
                    else:
                        self.dragged = 1 #dummy value to prevent new drag event.
                elif self.dragged != 1:
                    self.dragOver(self.internalPos, event.rel)
            else: 
                self.move(self.internalPos, event.rel)
        return []

    
    def draw(self, surface, rect = None):
        """draw(suface) -> draws subpanels to a buffer and draws that to the 
        surface."""
        rect = Rect(0,0, self.rect.width, self.rect.height)
        
        self.image.fill((0, 0, 0, 0))
        if self.bgColor:
            pygame.draw.rect(self.image, self.bgColor, rect)
        if self.drawBorder:
            pygame.draw.rect(self.image, self.color, rect, 1)
        for panel in self.panels:
            panel.draw(self.image, rect)
        if self.dragged and self.dragged != 1:
            self.dragged.draggingDraw(self)
        surface.blit(self.image, self.rect)


class Dragable(Panel):
    # move this point under the mouse hotspot.
    hotSpot = 0, 0
    drawBorderDragging = True

    def __init__(self, rect, parent):
        Panel.__init__(self, rect)
        self.parent = parent
        self.image = pygame.Surface(rect.size).convert()
        self.image.set_colorkey(BLACK)

    def drag(self, start):
        drag = Panel.drag(self, start)
        if drag:
            return drag
        return self, self.parent

    def draggingDraw(self, topLevelPanel):
        surface = topLevelPanel.image
        pos = (topLevelPanel.internalPos[0] - self.hotSpot[0],
               topLevelPanel.internalPos[1] - self.hotSpot[1])
        # draw self (floating):
        surface.blit(self.image, pos)
        if self.drawBorderDragging:
            rect = Rect(self.rect)
            rect.topleft = pos
            pygame.draw.rect(surface, self.color, rect, 1)
        # draw subpanels:
        for panel in self.panels:
            tmp = panel.rect.topleft
            panel.rect.left += pos[0] - self.rect.left
            panel.rect.top += pos[1] - self.rect.top
            panel.draw(surface, rect=None)
            panel.rect.topleft = tmp

    def handleKeys(self, keys):
        pass


class Slider(Panel):
    """
        a slider panel,
        takes a rect (for it's size)
        takes a handler function that is called upon change.
        a value of 0 through 1 is passed down to thing handler function.

        optional position. that is a value between 0 and 1.
        0 being set to the start of the slider,
        1 being set to the end of the slider.
        and any value inbetween 0 and 1, sets the slider
        to the relative position.

        optional hori value for setting the slider horizontal
        and vertical otherwise.
    """
    def __init__(self, rect, function, pos=0, hori=False):
        Panel.__init__(self, rect)
        # hori is for if the slider is horizontal
        # or not (if false then vertical)
        self.hori = hori
        # reference to handler function.
        self.function = function
        # get the relative position.
        x, y, width, height = self.rect
        self.pos = height*pos
        # create a initial rect for the dragable
        if self.hori:
            newrect = Rect(rect[0]+rect[2]-10+self.pos, rect[1]+(rect[3]/2)-10,
                           10, rect[3])
        else:
            newrect = Rect(rect[0]+(rect[2]/2)-10, rect[3]+rect[1]-10-self.pos,
                           rect[2], 10)
        self.dragable = Dragable(newrect, self)
        self.dragable.color = DRAGGABLE
        self.dragable.bgColor = BS1

        self.addPanel(self.dragable)
        self.function(pos)

    # def setPos(self, value):
    #     # create a initial rect for the dragable
    #     if self.hori:
    #         rect = Rect(rect[0]+rect[2]-10+self.pos, rect[1]+(rect[3]/2)-10,
    #                     10, rect[3])
    #     else:
    #         rect = Rect(rect[0]+(rect[2]/2)-10, rect[3]+rect[1]-10-self.pos,
    #                     rect[2], 10)
    #     self.dragable.rect = rect

    # def getPos(self):
    #     return self.pos

    def drop(self, pos, dropped):
        pass

    def dragOver(self, pos, rel):
        """called when the mouse moves to or from this panel."""
        oldpos = pos[0] - rel[0], pos[1] - rel[1]
        for panel in self.panels:
            if not panel.rect.collidepoint(oldpos) and not panel.rect.collidepoint(pos):
                if self.hori:
                    panel.rect[0] = oldpos[0] - panel.rect[2]
                    if self.rect[2] > (pos[0] - self.rect[0]) and self.rect[0] < pos[0]:
                        self.function((self.rect[2] - (pos[0] - self.rect[0]) + 0.001) / self.rect[2])
                else:
                    panel.rect[1] = oldpos[1] - panel.rect[3]
                    if self.rect[1] < pos[1] and self.rect[3] > (pos[1] - self.rect[1]):
                        self.function((self.rect[3] - (pos[1] - self.rect[1]) + 0.001) / self.rect[3])

    def click(self, button, pos):
        if self.hori:
            self.dragable.rect[0] = pos[0] - int(self.dragable.rect[2]/2)
            self.pos = ((self.rect[2] - (pos[0] - self.rect[0]) + 0.001) / self.rect[2])
            self.function(self.pos)
        else:
            self.dragable.rect[1] = pos[1] - int(self.dragable.rect[3]/2)
            self.pos = ((self.rect[3] - (pos[1] - self.rect[1]) + 0.001) / self.rect[3])
            self.function(self.pos)

    def handleKeys(self, keys):
        pass


class ColorPanel(Panel):
    def __init__(self, parent, rect, color):
        self.myColor = color
        self.parent = parent
        Panel.__init__(self, rect)

    def draw(self, surface, rect):
        pygame.draw.rect(surface, self.myColor, self.rect) 
        Panel.draw(self, surface, rect)


class Button(Panel):
    """Button(rect, function, text) -> a button that says text and does
    function when clicked. """
    activeColor = BUTTON_ACTIVE
    inactiveColor = BS1
    
    def __init__(self, rect, function, text, font = FONT, corners = [5,0,5,0]):
        Panel.__init__(self, rect, corners)
        self.function = function
        self.text = text
        self.color = self.inactiveColor
        if fontModule and text:
            self.image = font.render(self.text, True, self.color)
    
    def click(self, button, pos):
        """called when this panel is clicked on."""
        if button == 1:
            self.function()
            return True
        return Panel.click(self, button, pos)
    
    def move(self, pos, rel):
        """called when the mouse moves to or from this panel."""
        if self.rect.collidepoint(pos):
            self.color = self.activeColor
        else:
            self.color = self.inactiveColor
        Panel.move(self, pos, rel)


class ShapeButton(Button):
    """ShapeButton(rect, function, points) -> a button that looks like
    the line through points, is at rect, and does function when clicked.
    You may want to change self.activeColor, self.inactiveColor, or
    self.weight . """
    weight = 3
    activeColor = SBUTTON_ACTIVE
    inactiveColor = SBUTTON_INACTIVE
    
    
    def __init__(self, rect, function, points):
        Panel.__init__(self, rect)
        self.function = function
        self.points = points
        self.color = self.inactiveColor
        
    def draw(self, surface, rect):
        for point in self.points:
            if not rect.collidepoint(point):
                return
        pygame.draw.lines(surface, self.color, True, self.points, self.weight)


class InputField(Panel):
    drawBorder = False
    image = None
    
    def __init__(self, rect, game, function = None, font = BIG_FONT, color = BS1, width = 20):
        self.text = ""
        self.game = game
        self.function = function
        self.preftext = []
        self.newText = False
        self.index = 0
        self.cursorloc = 0
        self.width = width
        self.cursortimeout = 1
        self.color = color
        self.lineHeight = font.get_height()
        self.temprect = rect
        if not fontModule:
            return
        self.font = font
        Panel.__init__(self, rect, corners = [5,0,5,0])

    def getText(self):
        # thou shalt not erase the text history
        text = self.text
        if self.newText:
            self.newText = False
            self.text = ""
            return text

    def setText(self, text):
        pass
        #self.preftext = text

    def handleEvent(self, event):
        allowedkeys = list(range(97,122)) + list(range(32,71))
        if event.type == pygame.KEYDOWN:
            if event.key in allowedkeys and self.width >= len(self.text):
                length = len(self.text) - self.cursorloc
                one = self.text[:length]
                
                two = self.text[length:]
                self.text = one + event.unicode + two

            elif event.key == K_UP:
                if self.index > 0:
                    self.index -= 1
                    self.text = self.preftext[self.index]


            elif event.key == K_DOWN:
                if self.index < len(self.preftext)-1:
                    self.index += 1
                    self.text = self.preftext[self.index]
                elif self.index < len(self.preftext):
                    self.index += 1
                    self.text = ""
                    
            
            elif event.key == K_RETURN:
                self.newText = True
                if self.function:
                    self.function()

                self.preftext.append(self.text)
                self.index = len(self.preftext)
                

            elif event.key == K_BACKSPACE:
                one  = two = ''
                length = len(self.text) - self.cursorloc
                if length > 0:
                    one = self.text[:length-1]
                two = self.text[length:]
                self.text = one + two

            elif event.key == K_RIGHT and self.cursorloc > 0:
                self.cursorloc -= 1
                
            elif event.key == K_LEFT and self.cursorloc < len(self.text):
                self.cursorloc += 1

    def update(self):
        if self.cursortimeout <= 0.5:
            self.cursortimeout += 1.01 / self.game.fps
        else:
            self.cursortimeout = 0

        w,h = self.font.size(self.text)
        self.image = pygame.Surface((w+20,h),
        hardwareFlag | SRCALPHA).convert_alpha()
        y = 0
        
        cursorrect = Rect(w - self.cursoroffset() ,0,3,self.font.get_height())
        
        pygame.draw.rect(self.image, (255,255,255,self.cursortimeout*60), cursorrect)
        
        self.image.blit(self.font.render(self.text, True, self.color), (0, 0))

        # self.rect = Rect(self.temprect.topleft, self.image.get_size())

    def cursoroffset(self):
        length = len(self.text) - self.cursorloc
        return self.font.size(self.text[length:])[0]


class ScrollPanel(Panel):
    """A panel with a scrollbar."""
    scrollRate = 48
    def __init__(self, displayRect, fullDimensions):
        Panel.__init__(self, displayRect)
        fullRect = Rect(displayRect.left, displayRect.top, \
                        fullDimensions[0], fullDimensions[1])
        self.image = pygame.Surface(fullRect.size, \
                        hardwareFlag | SRCALPHA).convert_alpha()
        self.image.set_colorkey(BLACK)
        self.visibleRect = Rect((0, 0), displayRect.size)
        self.up = ShapeButton(Rect(self.rect.right - 14,\
                    self.rect.top, 14, 14),\
                    lambda: self.scroll(0, -ScrollPanel.scrollRate),\
                    ((self.rect.right - 8, self.rect.top + 2),\
                    (self.rect.right - 2, self.rect.top + 14),\
                    (self.rect.right - 14, self.rect.top + 14)))
        self.down = ShapeButton(Rect(self.rect.right - 14,\
                    self.rect.bottom - 28, 14, 14),\
                    lambda: self.scroll(0, ScrollPanel.scrollRate),\
                    ((self.rect.right - 8, self.rect.bottom - 16),\
                    (self.rect.right - 2, self.rect.bottom - 28),\
                    (self.rect.right - 14, self.rect.bottom - 28)))
        self.left = ShapeButton(Rect(self.rect.left, \
                    self.rect.bottom - 14, 14, 14),\
                    lambda: self.scroll(-ScrollPanel.scrollRate, 0),\
                    ((self.rect.left + 2, self.rect.bottom - 8),\
                    (self.rect.left + 14, self.rect.bottom - 2),\
                    (self.rect.left + 14, self.rect.bottom - 14)))
        self.right = ShapeButton(Rect(self.rect.right - 28,\
                    self.rect.bottom - 14, 14, 14),\
                    lambda: self.scroll(ScrollPanel.scrollRate, 0),\
                    ((self.rect.right - 16, self.rect.bottom - 8),\
                    (self.rect.right - 28, self.rect.bottom - 2),\
                    (self.rect.right - 28, self.rect.bottom - 14)))
        self.scrollButtons =[self.up, self.down, self.left, self.right]
        
    def scroll(self, x, y):
        """scroll this panel by x,y."""
        self.visibleRect.left = limit(0, self.visibleRect.left + x, \
                    self.image.get_width() - self.visibleRect.width)
        self.visibleRect.top = limit(0, self.visibleRect.top + y, \
                    self.image.get_height() - self.visibleRect.height)
        
    def draw(self, surface, rect):
        """draws this panel on the surface."""
        rect = rect.clip(self.rect)
        if self.drawBorder:
            pygame.draw.rect(surface, self.color, rect, 1)
        if self.bgColor:
            pygame.draw.rect(surface, self.bgColor, rect, 0)
            
        for panel in self.panels:
            panel.draw(self.image, self.visibleRect)
        surface.blit(self.image, self.rect, self.visibleRect)
        if self.image.get_height() > self.rect.height:
            self.up.draw(surface, rect)
            self.down.draw(surface, rect)
        if self.image.get_width() > self.rect.width:
            self.left.draw(surface, rect)
            self.right.draw(surface, rect)
        self.image.fill((0,0,0,0))
    
    def click(self, button, pos):
        """called when this panel is clicked on."""
        #scroll:
        if button == 4:
            if self.image.get_height() > self.rect.height:  #vertical
                self.scroll(0, -ScrollPanel.scrollRate)
                return True
            elif self.image.get_width() > self.rect.width:  #horizontal
                self.scroll(-ScrollPanel.scrollRate, 0)
                return True
        elif button == 5:
            if self.image.get_height() > self.rect.height:  #vertical
                self.scroll(0, ScrollPanel.scrollRate)
                return True
            elif self.image.get_width() > self.rect.width:  #horizontal
                self.scroll(ScrollPanel.scrollRate, 0)
                return True
        # click the scroll buttons if the image is larger than the visibleRect:
        if self.image.get_height() > self.rect.height:
            if self.up.rect.collidepoint(pos):
                return self.up.click(button, pos)
            if self.down.rect.collidepoint(pos):
                return self.down.click(button, pos)
        if self.image.get_width() > self.rect.width:
            if self.left.rect.collidepoint(pos):
                return self.left.click(button, pos)
            if self.right.rect.collidepoint(pos):
                return self.right.click(button, pos)
        #pass the click on to first colliding child:	
        pos = pos[0] - self.rect.left + self.visibleRect.left, \
                pos[1] - self.rect.top + self.visibleRect.top
        for panel in self.panels:
            if panel.rect.collidepoint(pos):
                if panel.click(button, pos):
                    return True
    
    def move(self, pos, rel):
        """called when the mouse moves to or from this panel."""
        oldpos = pos[0] - rel[0] , pos[1] - rel[1]
        #it's okay if invisible scroll buttons get highlighted.
        for panel in self.scrollButtons:
            if panel.rect.collidepoint(oldpos) or panel.rect.collidepoint(pos):
                panel.move(pos, rel)
        pos = pos[0] - self.rect.left + self.visibleRect.left, \
                pos[1] - self.rect.top + self.visibleRect.top
        oldpos = oldpos[0] - self.rect.left + self.visibleRect.left, \
                oldpos[1] - self.rect.top + self.visibleRect.top
        for panel in self.panels:
            if panel.rect.collidepoint(oldpos) or panel.rect.collidepoint(pos):
                panel.move(pos, rel)
                
    def dragOver(self, pos, rel):
        """called when the mouse moves to or from this panel."""
        oldpos = pos[0] - rel[0] , pos[1] - rel[1]
        #it's okay if invisible scroll buttons get highlighted.
        for panel in self.scrollButtons:
            if panel.rect.collidepoint(oldpos) or panel.rect.collidepoint(pos):
                panel.dragOver(pos, rel)
        pos = pos[0] - self.rect.left + self.visibleRect.left, \
                pos[1] - self.rect.top + self.visibleRect.top
        oldpos = oldpos[0] - self.rect.left + self.visibleRect.left, \
                oldpos[1] - self.rect.top + self.visibleRect.top
        for panel in self.panels:
            if panel.rect.collidepoint(oldpos) or panel.rect.collidepoint(pos):
                panel.dragOver(pos, rel)


class Selectable(Panel):
    activeColor = BUTTON_ACTIVE
    inactiveColor = BS1
    selectedColor = DS_SELECTED
    selected = False
    bgInactive = None
    bgActive = None
    bgSelected = None
    
    def __init__(self, rect):
        Panel.__init__(self, rect)
        self.color = self.inactiveColor
        
    def move(self, pos, rel):
        """called when the mouse moves to or from this panel."""
        if not self.selected and self.rect.collidepoint(pos):
            self.color = self.activeColor
            self.bgColor = self.bgActive
        elif not self.selected:
            self.color = self.inactiveColor
            self.bgColor = self.bgInactive
        Panel.move(self, pos, rel)
    
    def select(self):
        self.selected = True
        self.color = self.selectedColor
        self.bgColor = self.bgSelected
    
    def unselect(self):
        self.selected = False
        self.color = self.inactiveColor
        self.bgColor = self.bgInactive


class DragableSelectable(Dragable):
    activeColor = BUTTON_ACTIVE
    inactiveColor = BS1
    selectedColor = DS_SELECTED
    bgInactive = None
    bgActive = None
    bgSelected = None
    selected = False
    def __init__(self, rect, parent): 
        Dragable.__init__(self, rect, parent)
        self.color = self.inactiveColor
        
    def move(self, pos, rel):
        """called when the mouse moves to or from this panel."""
        if not self.selected and self.rect.collidepoint(pos):
            self.color = self.activeColor
            self.bgColor = self.bgActive
        elif not self.selected:
            self.color = self.inactiveColor
            self.bgColor = self.bgInactive
        Panel.move(self, pos, rel)
    
    def select(self):
        self.selected = True
        self.color = self.selectedColor
        self.bgColor = self.bgSelected
    
    def unselect(self):
        self.selected = False
        self.color = self.inactiveColor
        self.bgColor = self.bgInactive
                
    def endDrag(self, dragged, result):
        """called when a drag from here drops with a non-None result."""
        if result == 1:
            self.removePanel(dragged)
            self.removeSelectable(dragged)


class Selecter(ScrollPanel):
    selected = None
    selectables = []
    nextStart = 0
    def __init__(self, rect, vertical = True):
        """Selector(rect, vertical = True) -> A panel with selectable subpanels.
        The last selectable clicked is accesible as selector.selected.
        set vertical to false to have the selectables tile horizontally 
        instead."""
        ScrollPanel.__init__(self, rect, rect.size)
        self.vertical = vertical
        
    def setSelected(self, selectable):
        """changes which selectable is selected by this selecter.
        Called by Selector.click()."""
        #unselect old:
        if self.selected:
            self.selected.unselect()
        self.selected = selectable
        if self.selected:
            self.selected.select()
        
    def drag(self, start):
        result = ScrollPanel.drag(self, start)
        if result: return result
        posNew = start[0] - self.rect.left + self.visibleRect.left, \
                start[1] - self.rect.top + self.visibleRect.top
        #check selected first:
        if self.selected and self.selected.rect.collidepoint(posNew):
            dragged = self.selected.drag(posNew)
            if dragged:
                return dragged
        for selectable in self.selectables:
            if selectable.rect.collidepoint(posNew):
                result = selectable.drag(posNew)
                if result: return result
        
    def drop(self, pos, dropped):
        posNew = pos[0] - self.rect.left + self.visibleRect.left, \
                pos[1] - self.rect.top + self.visibleRect.top
        #check selected first:
        if self.selected and self.selected.rect.collidepoint(posNew):
            result = self.selected.drop(posNew, dropped)
            if result:
                return result
        for selectable in self.selectables:
            if selectable.rect.collidepoint(posNew):
                result = selectable.drop(posNew, dropped)
                if result: return result

    def click(self, button, pos):
        if ScrollPanel.click(self, button, pos):
            return True
        posNew = pos[0] - self.rect.left + self.visibleRect.left, \
                pos[1] - self.rect.top + self.visibleRect.top
        new = False
        for selectable in self.selectables:
            if selectable.rect.collidepoint(posNew) and button == 1:
                self.setSelected(selectable)
                new = True
        return new
        
    def addSelectable(self, selectable):
        """Adds a new selectable to this selecter.  Sets the selectable's rect
        left or top to the first empty position, maybe extends this selecter's 
        scrolling image to be big enough."""
        if self.vertical:
            y = 2
            for panel in self.selectables:
                y += panel.rect.height + 2 #might have different heights.
            offset = y - selectable.rect.top
            selectable.rect.top = y
            for panel in selectable.panels:
                panel.rect.top += offset
            if self.image.get_height() < y:
                self.image = pygame.Surface((self.image.get_width(),\
                        y * 1.5), hardwareFlag | SRCALPHA).convert_alpha()
                self.image.set_colorkey(BLACK)
        else: #horizontal
            x = 2
            for panel in self.selectables:
                x += panel.rect.width + 2
            offset = x - selectable.rect.left
            selectable.rect.left = x
            for panel in selectable.panels:
                panel.rect.left += offset
            if self.image.get_width() < x:
                self.image = pygame.Surface((x * 1.5,\
                        self.image.get_height()), hardwareFlag | SRCALPHA).convert_alpha()
                self.image.set_colorkey(BLACK)
        self.selectables.append(selectable)
        
    def removeSelectable(self, selectable):
        """removes a selectable and calls reset."""
        if selectable in self.selectables:
            self.selectables.remove(selectable)
        self.reset()
        
    def reset(self):
        """Re-adds all the selectables.  Called by 
        removeSelectable() to remove empty spaces."""
        self.selected = None
        if self.vertical:
            y = 2
            for panel in self.selectables:
                offset = y - panel.rect.top
                panel.rect.top = y
                for subpanel in panel.panels:
                    subpanel.rect.top += offset
                y += panel.rect.height + 2
            #shrink full image:
            if self.image.get_height() < y:
                self.image = pygame.Surface((self.image.get_width(),\
                        y * 1.5), hardwareFlag | SRCALPHA).convert_alpha()
                self.image.set_colorkey(BLACK)
            #grow full image:
            if self.image.get_height() > y * 3:
                self.image = pygame.Surface((self.image.get_width(),\
                        y * 1.5), hardwareFlag | SRCALPHA).convert_alpha()
                self.image.set_colorkey(BLACK)
                # if the new real image is smaller than the visible image, 
                #set the offset to 0.
                if self.image.get_height() < self.visibleRect.height:
                    self.visibleRect.top = 0
        else: #horizontal
            x = 2
            for panel in self.selectables:
                offset = x - panel.rect.left
                panel.rect.left = x
                for subpanel in panel.panels:
                    subpanel.rect.left += offset
                x += panel.rect.width + 2
            #shrink full image:
            if self.image.get_width() < x:
                self.image = pygame.Surface((x * 1.5,\
                        self.image.get_height()), hardwareFlag | SRCALPHA)\
                        .convert_alpha()
                self.image.set_colorkey(BLACK)
            #grow full image:
            if self.image.get_width() > x * 3:
                self.image = pygame.Surface((x * 1.5,\
                        self.image.get_height()), hardwareFlag | SRCALPHA).convert_alpha()
                self.image.set_colorkey(BLACK)
                # if the new real image is smaller than the visible image, 
                #set the offset to 0.
                if self.image.get_width() < self.visibleRect.width:
                    self.visibleRect.left = 0
        Panel.reset(self)
    
    def move(self, pos, rel):
        oldpos = pos[0] - rel[0] , pos[1] - rel[1]
        posNew = pos[0] - self.rect.left + self.visibleRect.left, \
                pos[1] - self.rect.top + self.visibleRect.top
        oldposNew = oldpos[0] - self.rect.left + self.visibleRect.left, \
                oldpos[1] - self.rect.top + self.visibleRect.top
        for panel in self.selectables:
            if panel.rect.collidepoint(oldposNew) \
            or panel.rect.collidepoint(posNew):
                panel.move(posNew, rel)
            ScrollPanel.move(self, pos, rel)
            
    def dragOver(self, pos, rel):
        oldpos = pos[0] - rel[0] , pos[1] - rel[1]
        posNew = pos[0] - self.rect.left + self.visibleRect.left, \
                pos[1] - self.rect.top + self.visibleRect.top
        oldposNew = oldpos[0] - self.rect.left + self.visibleRect.left, \
                oldpos[1] - self.rect.top + self.visibleRect.top
        for panel in self.selectables:
            if panel.rect.collidepoint(oldposNew) \
            or panel.rect.collidepoint(posNew):
                panel.dragOver(posNew, rel)
            ScrollPanel.dragOver(self, pos, rel)
                
    def draw(self, surface, rect):
        """draws this panel on the surface."""
        for panel in self.selectables:
            panel.draw(self.image, self.visibleRect)
        ScrollPanel.draw(self, surface, rect)


class Label(Panel):
    """Label(self,  rect, text, color = BS1, font = FONT) ->
    A panel with a single line of text."""
    drawBorder = False
    def __init__(self, rect, text, font = FONT, color = BS1,corners = [5,0,5,0]):
        Panel.__init__(self, rect,corners)
        self.text = text
        self.color = color
        if fontModule:
            self.image = font.render(self.text, True, self.color)
            self.rect = Rect(rect.topleft, self.image.get_size())


class FunctionLabel(Panel):
    """A label that updates its text by calling a string function."""
    drawBorder = False
    def __init__(self, rect, textFunction, font = FONT, corners=[5,0,5,0]):
        Panel.__init__(self, rect)
        self.textFunction = textFunction
        self.font = font
        self.update()
        
    def update(self):
        if fontModule:
            self.image = self.font.render(self.textFunction(), True, self.color)


class TextBlock(Panel):
    """TextBlock(self,  rect, text, font = FONT) 
    A panel with multi-line text. rect height is reset based on font and 
    number of lines in text."""

    drawBorder = False
    image = None
    def __init__(self, rect, textFunction, font = FONT, color = BLACK, width = 200, corners=[5,0,5,0]):
        self.textFunction = textFunction
        self.color = color
        self.lineHeight = font.get_height()
        self.temprect = rect
        if not fontModule:
            return
        self.font = font
        Panel.__init__(self, rect,corners)

    def update(self):
        if isinstance(self.textFunction, basestring):
            self.image = pygame.Surface((self.temprect.width, self.lineHeight * len(self.textFunction.split("\n"))),
            hardwareFlag | SRCALPHA).convert_alpha()
            y = 0
            for line in self.textFunction.split("\n"):
                self.image.blit(self.font.render(line, True, self.color), (0, y))
                y += self.lineHeight
            self.rect = Rect(self.temprect.topleft, self.image.get_size())
        else:
            self.image = pygame.Surface((self.temprect.width, self.lineHeight * len(self.textFunction().split("\n"))),
            hardwareFlag | SRCALPHA).convert_alpha()
            y = 0
            for line in self.textFunction().split("\n"):
                self.image.blit(self.font.render(line, True, self.color), (0, y))
                y += self.lineHeight
            self.rect = Rect(self.temprect.topleft, self.image.get_size())
