import SwiftUI


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
