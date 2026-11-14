import Foundation
import SoundAnalysis
import AVFoundation
class Obs: NSObject, SNResultsObserving {
  func request(_ r: SNRequest, didProduce res: SNResult) {
    guard let c = res as? SNClassificationResult else { return }
    let t = c.timeRange.start.seconds
    let top = c.classifications.prefix(4).filter{ $0.confidence > 0.15 }.map{ "\($0.identifier) \(Int($0.confidence*100))" }
    if !top.isEmpty { print(String(format: "%.1f", t), top.joined(separator: ", ")) }
  }
}
let url = URL(fileURLWithPath: CommandLine.arguments[1])
let a = try SNAudioFileAnalyzer(url: url)
let req = try SNClassifySoundRequest(classifierIdentifier: .version1)
req.windowDuration = CMTime(seconds: 1.0, preferredTimescale: 48000)
req.overlapFactor = 0.5
let o = Obs()
try a.add(req, withObserver: o)
a.analyze()
