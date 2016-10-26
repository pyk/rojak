package id.artificialintelligence.rojak.data.remote;

import java.util.List;

import id.artificialintelligence.rojak.models.Candidate;
import id.artificialintelligence.rojak.models.Media;
import retrofit2.http.GET;
import retrofit2.http.Path;
import rx.Observable;

public interface ApiService {

    @GET("candidates")
    Observable<List<Candidate>> getCandidateList();

    @GET("candidates/{id}")
    Observable<Candidate> getCandidate(@Path("id") int candidateId);

    @GET("media")
    Observable<List<Media>> getMediaList();

    @GET("media/{id}")
    Observable<Media> getMedia(@Path("id") int mediaId);
}
