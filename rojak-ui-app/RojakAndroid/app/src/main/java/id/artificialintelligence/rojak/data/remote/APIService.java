package id.artificialintelligence.rojak.data.remote;

import java.util.List;

import id.artificialintelligence.rojak.models.Candidate;
import id.artificialintelligence.rojak.models.Media;
import id.artificialintelligence.rojak.models.News;
import id.artificialintelligence.rojak.models.PairOfCandidates;
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

    @GET("news")
    Observable<List<News>> getNewsList();

    @GET("news/{id}")
    Observable<News> getNews(@Path("id") int newsId);

    @GET("pairings")
    Observable<List<PairOfCandidates>> getPairingList();

    @GET("pairings/{id}")
    Observable<PairOfCandidates> getPairing(@Path("id") int pairingId);
}
