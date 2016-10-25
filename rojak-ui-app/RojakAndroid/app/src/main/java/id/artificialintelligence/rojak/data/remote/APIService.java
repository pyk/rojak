package id.artificialintelligence.rojak.data.remote;

import java.util.List;

import id.artificialintelligence.rojak.models.Media;
import retrofit2.http.GET;
import retrofit2.http.Path;
import rx.Observable;

public interface ApiService {

    @GET("media")
    Observable<List<Media>> getMediaList();

    @GET("media/{id}")
    Observable<Media> getMedia(@Path("id") int mediaId);
}
