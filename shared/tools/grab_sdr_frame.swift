import AVFoundation; import AppKit
// usage: grab <video> <seconds> <out.png>
let a=CommandLine.arguments
let g=AVAssetImageGenerator(asset: AVURLAsset(url: URL(fileURLWithPath:a[1])))
g.appliesPreferredTrackTransform=true; g.requestedTimeToleranceBefore = .zero; g.requestedTimeToleranceAfter = .zero
let cg=try! g.copyCGImage(at: CMTime(seconds: Double(a[2])!, preferredTimescale: 600), actualTime: nil)
let rep=NSBitmapImageRep(cgImage: cg)
try! rep.representation(using:.png, properties:[:])!.write(to: URL(fileURLWithPath:a[3]))
print(cg.width, cg.height)
