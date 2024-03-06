if player.x < pickupcoin.x and 

if playerYPosition < (blockYPosition + pixel):
 
      if ((playerXPosition > blockXPosition
           and playerXPosition < (blockXPosition + pixel))
          or ((playerXPosition + pixel) > blockXPosition
           and (playerXPosition + pixel) < (blockXPosition + pixel))):
 
          blockYPosition = height + 1000


def hasCollided(a, b) -> bool:
    """
    Checks collision between object a and b, returns true if collided, false if not.
    Objects must have x, y, width and height.

    Code from:
    "https://stackoverflow.com/questions/2440377/javascript-collision-detection"
    """
    return not (
        ((a.y + a.height) < b.y)
        or (a.y > (b.y + b.height))
        or ((a.x + a.width) < b.x)
        or (a.x > (b.x + b.width))
    )
