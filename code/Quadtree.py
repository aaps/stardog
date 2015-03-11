class QuadTree(object):
    """An implementation of a quad-tree.
 
    This QuadTree started life as a version of [1] but found a life of its own
    when I realised it wasn't doing what I needed. It is intended for static
    geometry, ie, items such as the landscape that don't move.
 
    This implementation inserts items at the current level if they overlap all
    4 sub-quadrants, otherwise it inserts them recursively into the one or two
    sub-quadrants that they overlap.
 
    Items being stored in the tree must possess the following attributes:
 
        left - the x coordinate of the left edge of the item's bounding box.
        top - the y coordinate of the top edge of the item's bounding box.
        right - the x coordinate of the right edge of the item's bounding box.
        bottom - the y coordinate of the bottom edge of the item's bounding box.
 
        where left < right and top < bottom
        
    ...and they must be hashable.
    
    Acknowledgements:
    [1] http://mu.arete.cc/pcr/syntax/quadtree/1/quadtree.py
    """
    def __init__(self, items, depth=2, bounding_rect=None):
        """Creates a quad-tree.
 
        @param items:
            A sequence of items to store in the quad-tree. Note that these
            items must possess left, top, right and bottom attributes.
            
        @param depth:
            The maximum recursion depth.
            
        @param bounding_rect:
            The bounding rectangle of all of the items in the quad-tree. For
            internal use only.
        """
        self.depth = depth
        self.bounding_rect = bounding_rect
        # self.items = None
        # The sub-quadrants are empty to start with.
        self.nw = self.ne = self.se = self.sw = None
        # If we've reached the maximum depth then insert all items into this
        # quadrant.
        self.depth -= 1
        if self.depth == 0:
            self.items = items
            return

        self.reset(items)
 

    def reset(self, items):
        # Find this quadrant's centre.
        if self.bounding_rect:
            l, t, r, b = self.bounding_rect
        else:
            # If there isn't a bounding rect, then calculate it from the items.
            l = min(item.rect.left for item in items)
            t = min(item.rect.top for item in items)
            r = max(item.rect.right for item in items)
            b = max(item.rect.bottom for item in items)
        cx = self.cx = (l + r) * 0.5
        cy = self.cy = (t + b) * 0.5
        
        self.items = []
        self.nw_items = []
        self.ne_items = []
        self.se_items = []
        self.sw_items = []
        
        for item in items:
            # Which of the sub-quadrants does the item overlap?
            in_nw = item.rect.left <= cx and item.rect.top <= cy
            in_sw = item.rect.left <= cx and item.rect.bottom >= cy
            in_ne = item.rect.right >= cx and item.rect.top <= cy
            in_se = item.rect.right >= cx and item.rect.bottom >= cy
                
            # If it overlaps all 4 quadrants then insert it at the current
            # depth, otherwise append it to a list to be inserted under every
            # quadrant that it overlaps.
            if in_nw and in_ne and in_se and in_sw:
                self.items.append(item)
            else:
                if in_nw: self.nw_items.append(item)
                if in_ne: self.ne_items.append(item)
                if in_se: self.se_items.append(item)
                if in_sw: self.sw_items.append(item)
            
        # Create the sub-quadrants, recursively.
        if self.nw_items:
            self.nw = QuadTree(self.nw_items, self.depth, (l, t, cx, cy))
        if self.ne_items:
            self.ne = QuadTree(self.ne_items, self.depth, (cx, t, r, cy))
        if self.se_items:
            self.se = QuadTree(self.se_items, self.depth, (cx, cy, r, b))
        if self.sw_items:
            self.sw = QuadTree(self.sw_items, self.depth, (l, cy, cx, b))


    def hit(self, rect):
        """Returns the items that overlap a bounding rectangle.
 
        Returns the set of all items in the quad-tree that overlap with a
        bounding rectangle.
        
        @param rect:
            The bounding rectangle being tested against the quad-tree. This
            must possess left, top, right and bottom attributes.
        """
        def overlaps(item):
            return rect.right >= item.rect.left and rect.left <= item.rect.right and \
                   rect.bottom >= item.rect.top and rect.top <= item.rect.bottom
        
        # Find the hits at the current level.
        hits = set(item for item in self.items if overlaps(item))
        # Recursively check the lower quadrants.
        if self.nw and rect.left <= self.cx and rect.top <= self.cy:
            hits |= self.nw.hit(rect)
        if self.sw and rect.left <= self.cx and rect.bottom >= self.cy:
            hits |= self.sw.hit(rect)
        if self.ne and rect.right >= self.cx and rect.top <= self.cy:
            hits |= self.ne.hit(rect)
        if self.se and rect.right >= self.cx and rect.bottom >= self.cy:
            hits |= self.se.hit(rect)
 
        return hits