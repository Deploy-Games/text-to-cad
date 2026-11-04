FeatureScript 2444;
import(path : "onshape/std/common.fs", version : "2444.0");

/**
 * Parametric Desk Storage Frame Feature for Onshape Part Studios.
 * Reconstructed from concept sketch: 1600 x 800 x 300 mm with 6 partitioned bays.
 * 
 * Usage in Onshape:
 * 1. In your Onshape document, click '+' at bottom-left and select 'Create Feature Studio'.
 * 2. Paste this entire code and click 'Commit'.
 * 3. Switch back to your Part Studio. A new 'Desk Storage Frame' button will appear in the toolbar.
 * 4. Click it to insert the fully parametric feature into your Feature Tree!
 */
annotation { "Feature Type Name" : "Desk Storage Frame", "Feature Type Description" : "Parametric partitioned desk frame (1600x800x300mm, 6 bays)" }
export const deskStorageFrame = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Overall Length (X)" }
        isLength(definition.overallLength, { (millimeter) : [100, 1600, 5000] } as LengthBoundSpec);

        annotation { "Name" : "Overall Depth (Y)" }
        isLength(definition.overallDepth, { (millimeter) : [100, 800, 5000] } as LengthBoundSpec);

        annotation { "Name" : "Overall Height (Z)" }
        isLength(definition.overallHeight, { (millimeter) : [50, 300, 2000] } as LengthBoundSpec);

        annotation { "Name" : "Wall Thickness" }
        isLength(definition.wallThickness, { (millimeter) : [5, 18, 50] } as LengthBoundSpec);

        annotation { "Name" : "Bottom Thickness" }
        isLength(definition.bottomThickness, { (millimeter) : [5, 18, 50] } as LengthBoundSpec);
    }
    {
        // 1. Create outer bounding solid block
        fCuboid(context, id + "baseBlock", {
            "corner1" : vector(0, 0, 0) * millimeter,
            "corner2" : vector(definition.overallLength, definition.overallDepth, definition.overallHeight)
        });

        // 2. Cut out the 6 interior compartment bays leaving uniform wall thickness
        var zBottom = definition.bottomThickness;
        var zTop = definition.overallHeight + 1.0 * millimeter;

        var xDiv1 = 400.0 * millimeter;
        var xDiv2 = 1000.0 * millimeter;
        var xDiv3 = 1200.0 * millimeter;
        var yDiv = 400.0 * millimeter;
        var halfWall = definition.wallThickness / 2.0;

        var pockets = [
            // Bay 1: Left full-depth bay (400 x 800 mm)
            [definition.wallThickness, xDiv1 - halfWall, definition.wallThickness, definition.overallDepth - definition.wallThickness],
            // Bay 2: Rear center-left bay (600 x 400 mm)
            [xDiv1 + halfWall, xDiv2 - halfWall, yDiv + halfWall, definition.overallDepth - definition.wallThickness],
            // Bay 3: Rear center-right bay (200 x 400 mm)
            [xDiv2 + halfWall, xDiv3 - halfWall, yDiv + halfWall, definition.overallDepth - definition.wallThickness],
            // Bay 4: Front center bay (800 x 400 mm)
            [xDiv1 + halfWall, xDiv3 - halfWall, definition.wallThickness, yDiv - halfWall],
            // Bay 5: Rear right bay (400 x 400 mm)
            [xDiv3 + halfWall, definition.overallLength - definition.wallThickness, yDiv + halfWall, definition.overallDepth - definition.wallThickness],
            // Bay 6: Front right bay (400 x 400 mm)
            [xDiv3 + halfWall, definition.overallLength - definition.wallThickness, definition.wallThickness, yDiv - halfWall]
        ];

        for (var i = 0; i < size(pockets); i += 1)
        {
            var p = pockets[i];
            var pocketId = id + ("pocket" ~ i);
            fCuboid(context, pocketId, {
                "corner1" : vector(p[0], p[2], zBottom),
                "corner2" : vector(p[1], p[3], zTop)
            });

            opBoolean(context, id + ("boolCut" ~ i), {
                "tools" : qCreatedBy(pocketId, EntityType.BODY),
                "targets" : qCreatedBy(id + "baseBlock", EntityType.BODY),
                "operationType" : BooleanOperationType.SUBTRACTION
            });
        }
    });
