package id.artificialintelligence.rojak.di.module;

import android.content.Context;

import java.util.concurrent.TimeUnit;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;
import id.artificialintelligence.rojak.BuildConfig;
import id.artificialintelligence.rojak.data.local.PreferencesHelper;
import id.artificialintelligence.rojak.data.remote.ApiService;
import id.artificialintelligence.rojak.data.remote.UnauthorisedInterceptor;
import okhttp3.Cache;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Retrofit;
import retrofit2.adapter.rxjava.RxJavaCallAdapterFactory;
import retrofit2.converter.gson.GsonConverterFactory;

@Module
public class NetworkModule {

    private static final String ENDPOINT = BuildConfig.BASE_URL;
    private static final String KEY = BuildConfig.KEY;

    @Singleton
    @Provides
    OkHttpClient provideOkHttpClient(Context context) {
        OkHttpClient.Builder builder = new OkHttpClient().newBuilder();

        if (BuildConfig.DEBUG) {
            HttpLoggingInterceptor interceptor = new HttpLoggingInterceptor();
            interceptor.setLevel(HttpLoggingInterceptor.Level.BASIC);
            builder.addInterceptor(interceptor);
        }

        //Extra Headers
        builder.addNetworkInterceptor(chain -> {
            if (PreferencesHelper.getString(context, KEY) == null) {
                PreferencesHelper.putString(context, KEY, "");
            }

            Request request = chain.request().newBuilder()
                    .addHeader("Authorization", PreferencesHelper.getString(context, KEY))
                    .build();

            return chain.proceed(request);
        });

        int cacheSize = 10 * 1024 * 1024; // 10 MiB
        Cache cache = new Cache(context.getCacheDir(), cacheSize);
        builder.cache(cache);

        return builder.readTimeout(30, TimeUnit.SECONDS)
                .connectTimeout(20, TimeUnit.SECONDS)
                .writeTimeout(60, TimeUnit.SECONDS)
                .addInterceptor(new UnauthorisedInterceptor(context))
                .build();
    }

    @Singleton
    @Provides
    Retrofit provideRetrofit(OkHttpClient okHttpClient) {
        return new Retrofit.Builder()
                .baseUrl(ENDPOINT)
                .client(okHttpClient)
                .addConverterFactory(GsonConverterFactory.create())
                .addCallAdapterFactory(RxJavaCallAdapterFactory.create())
                .build();
    }

    @Singleton
    @Provides
    ApiService provideApiService(Retrofit retrofit) {
        return retrofit.create(ApiService.class);
    }
}
