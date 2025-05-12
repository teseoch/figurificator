import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 12

from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()
import json

output_path = '.'   # TODO: set your own output path here!
filename = 'test.json'

renderView = GetActiveView()

out = {
    "CameraPosition":renderView.CameraPosition.GetData(),
    "CameraFocalPoint":renderView.CameraFocalPoint.GetData(),
    "CameraParallelScale":renderView.CameraParallelScale,
    "CameraParallelProjection":renderView.CameraParallelProjection,
    "CameraViewAngle":renderView.CameraViewAngle,
    "CameraViewUp":renderView.CameraViewUp.GetData(),
    "ViewSize":renderView.ViewSize.GetData(),
}

# Active source is important!!!
reader = GetActiveSource() 
view = GetActiveView()
times = reader.TimestepValues

meshes = []

for t in range(len(times)):
    view.ViewTime = times[t]
    Render()

    for source_name in GetSources():
        source = GetSources()[source_name]
        dp=GetDisplayProperties(source)
        col = dp.ColorArrayName
        dim = col[0]
        col = col[1]

        if dp.Visibility == 0:
            continue

        extractSurface = ExtractSurface(registrationName=source_name[0]+'_surf', Input=source)

        colLut = GetColorTransferFunction(col)

        # save data
        mesh = f'{output_path}{source_name[0]}_{t}.ply'
        SaveData(mesh, proxy=extractSurface,
            EnableColoring=1,
            ColorArrayName=[dim, col],
            LookupTable=colLut)
        meshes.append('{source_name[0]}.ply')

        Delete(extractSurface)
        del extractSurface


out['Meshes'] = meshes

with open(os.path.join(output_path, filename), 'w') as f:
    json.dump(out, f)