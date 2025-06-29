//
//  MainView.swift
//  SightLine
//
//  Created by Zoraz  on 6/20/25.
//

// MainView.swift
// MainView.swift
import SwiftUI

/// Main targeting interface - placeholder
struct MainView: View {
    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
            VStack(spacing: 20) {
                Text("Main Targeting View")
                    .font(.largeTitle)
                    .foregroundColor(.white)
                Text("Video feed and controls go here.")
                    .foregroundColor(.gray)
            }
        }
        .navigationTitle("Sightline")
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView()
    }
}
