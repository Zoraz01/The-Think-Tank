//
//  Item.swift
//  SightLine
//
//  Created by Zoraz  on 6/20/25.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
